# agents/supervisor.py
from typing import TypedDict, Annotated, List
import operator
from datetime import datetime
from langchain_core.messages import AnyMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import JsonOutputParser

from tools.web_agent import WebAgent
from tools.calendar_agent import CalendarAgent
from tools.suggestion_agent import SuggestionAgent
from core.db import add_task_to_db, get_all_tasks_from_db, reschedule_task_in_db

class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    next: str

class Supervisor:
    def __init__(self):
        self.web_agent = WebAgent()
        self.calendar_agent = CalendarAgent()
        self.suggestion_agent = SuggestionAgent()
        self.workflow = self._create_workflow()

    def _task_manager_tool(self, prompt: str) -> str:
        prompt = prompt.lower()
        if "reschedule task id" in prompt and "to" in prompt:
            try:
                task_id = int(prompt.split("id")[1].split("to")[0].strip())
                date_str = prompt.split("to")[1].strip()
                new_date = datetime.strptime(date_str, "%Y-%m-%d")
                reschedule_task_in_db(task_id, new_date)
                return f"Task {task_id} rescheduled to {date_str}."
            except Exception as e: return f"Error: {e}. Use format: 'reschedule task id X to YYYY-MM-DD'."
        if "add task:" in prompt:
            desc = prompt.split(":", 1)[1].strip()
            if desc: add_task_to_db(description=desc); return f"Added task: '{desc}'"
            return "Cannot add an empty task."
        if "show tasks" in prompt or "list tasks" in prompt:
            tasks = get_all_tasks_from_db()
            if not tasks: return "You have no tasks."
            return "Current tasks:\n" + "\n".join([f"- ID {t.id}: {t.description} {'(Completed)' if t.completed else ''}" for t in tasks])
        return "Unrecognized task command. Try 'add task:', 'show tasks', or 'reschedule...'"

    def _create_workflow(self):
        router_model = ChatOllama(model="phi3:mini", format="json")
        
        system_prompt = (
            "You are an expert AI router. Your job is to analyze the user's request and route it to the correct specialist agent. "
            "The available agents are: 'web_search' for internet questions, 'calendar_manager' for scheduling or checking events, "
            "'task_manager' for managing a to-do list, and 'end_conversation' for simple greetings or farewells.\n"
            "You MUST respond with a JSON object containing a single key 'next' with the name of the chosen agent. "
            "For example: {{\"next\": \"task_manager\"}}"
        )

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])

        parser = JsonOutputParser()
        routing_chain = prompt_template | router_model | parser

        graph = StateGraph(AgentState)

        def supervisor_node(state: AgentState):
            response = routing_chain.invoke({"messages": state["messages"]})
            return {"next": response['next']}

        def agent_node(state: AgentState, tool):
            user_prompt = state["messages"][-1].content
            result = tool(user_prompt)
            suggestion = self.suggestion_agent.provide_suggestion(user_prompt)
            final_response = f"{result}\n\n{suggestion}" if suggestion else result
            return {"messages": [HumanMessage(content=final_response.strip())]}

        def end_node(state: AgentState):
            return {"messages": [HumanMessage(content="Of course. Is there anything else I can help you with?")]}

        graph.add_node("supervisor", supervisor_node)
        graph.add_node("web_search", lambda s: agent_node(s, self.web_agent.search))
        graph.add_node("task_manager", lambda s: agent_node(s, self._task_manager_tool))
        graph.add_node("calendar_manager", lambda s: agent_node(s, self.calendar_agent.check_availability))
        graph.add_node("end_conversation", end_node)

        graph.set_entry_point("supervisor")
        graph.add_conditional_edges("supervisor", lambda s: s["next"], {
            "web_search": "web_search", "task_manager": "task_manager",
            "calendar_manager": "calendar_manager", "end_conversation": "end_conversation"
        })
        
        for tool in ["web_search", "task_manager", "calendar_manager", "end_conversation"]:
            graph.add_edge(tool, END)

        return graph.compile()

    def run(self, prompt: str):
        state = {"messages": [HumanMessage(content=prompt)]}
        final_state = self.workflow.invoke(state, {"recursion_limit": 5})
        return final_state['messages'][-1].content if final_state['messages'] else "Sorry, I encountered an issue."