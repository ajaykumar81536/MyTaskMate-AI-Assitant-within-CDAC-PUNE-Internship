# core/state.py
import reflex as rx
import asyncio
import os
from typing import List, Dict, Any
from core.db import TaskModel, get_all_tasks_from_db, update_task_status_in_db, TaskStatus
from agents.supervisor import Supervisor

class TaskDisplayModel(TaskModel):
    formatted_due_date: str

class ChatMessage(rx.Base):
    role: str
    content: str
    bg_image: str | None = None

class AppState(rx.State):
    tasks: List[TaskModel] = []
    chat_history: List[ChatMessage] = [
        ChatMessage(role="ai", content="### Welcome to MyTaskMate!\nHow can I assist you today?", bg_image="/abstract_bg.jpg"),
    ]
    prompt_text: str = ""
    is_processing: bool = False
    _supervisor: Supervisor | None = None
    uploaded_file_path: str | None = None

    async def on_load(self):
        await self.get_tasks()
        if self._supervisor is None:
            self._supervisor = Supervisor()

    async def get_tasks(self):
        db_tasks = get_all_tasks_from_db()
        self.tasks = [
            TaskModel(id=t.id, description=t.description, status=t.status.value, due_date=t.due_date, completed=t.completed)
            for t in db_tasks
        ]

    async def toggle_task_status(self, task: TaskModel):
        new_status = TaskStatus.COMPLETED if TaskStatus(task.status) != TaskStatus.COMPLETED else TaskStatus.PENDING
        update_task_status_in_db(task.id, new_status)
        await self.get_tasks()

    @rx.var
    def completed_tasks_count(self) -> int:
        return sum(1 for task in self.tasks if task.completed)

    @rx.var
    def pending_tasks_count(self) -> int:
        return len(self.tasks) - self.completed_tasks_count
    
    @rx.var
    def pending_tasks_list(self) -> List[TaskModel]:
        return [task for task in self.tasks if not task.completed]

    @rx.var
    def tasks_with_formatted_dates(self) -> List[TaskDisplayModel]:
        display_list = []
        for task in self.tasks:
            formatted_date = f"Due: {task.due_date.strftime('%Y-%m-%d')}" if task.due_date else "No due date"
            display_list.append(TaskDisplayModel(**task.dict(), formatted_due_date=formatted_date))
        return display_list
    
    async def handle_send(self):
        if not self.prompt_text.strip(): return
        self.is_processing = True
        self.chat_history.append(ChatMessage(role="user", content=self.prompt_text))
        self.chat_history.append(ChatMessage(role="ai", content=""))
        prompt_to_process = self.prompt_text
        self.prompt_text = ""
        yield

        try:
            if self._supervisor:
                response = self._supervisor.run(prompt_to_process)
                for char in response:
                    self.chat_history[-1].content += char
                    await asyncio.sleep(0.005); yield
                if "task" in prompt_to_process.lower():
                    await self.get_tasks()
        except Exception as e:
            self.chat_history[-1].content = f"An error occurred: {e}"
        finally:
            self.is_processing = False

    async def handle_upload(self, files: List[rx.UploadFile]):
        if not files: return
        uploaded_file = files[0]
        upload_dir = rx.get_upload_dir()
        os.makedirs(upload_dir, exist_ok=True)
        permanent_file_path = os.path.join(upload_dir, uploaded_file.filename)
        file_content = await uploaded_file.read()
        with open(permanent_file_path, "wb") as f: f.write(file_content)
        self.uploaded_file_path = permanent_file_path
        self.chat_history.append(ChatMessage(role="ai", content=f"File '{uploaded_file.filename}' ready. Document analysis is under construction."))