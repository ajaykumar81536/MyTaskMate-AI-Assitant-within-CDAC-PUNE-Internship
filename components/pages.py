# components/pages.py
import reflex as rx
from core.state import AppState

def tasks_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Task Management", size="8"),
        rx.card(
            rx.cond(
                AppState.tasks.length() > 0,
                rx.ordered_list(
                    rx.foreach(
                        AppState.tasks_with_formatted_dates,
                        lambda task: rx.list_item(
                            rx.hstack(
                                rx.checkbox(is_checked=task.completed, on_change=lambda _: AppState.toggle_task_status(task)),
                                rx.text(task.description, as_=rx.cond(task.completed, "s", "span")),
                                rx.spacer(),
                                rx.text(task.formatted_due_date, size="2"),
                                align="center", width="100%",
                            )
                        )
                    )
                ),
                rx.text("No tasks found. Add one via the chat!"),
            )
        ),
        width="100%", max_width="900px", align="start", spacing="5",
    )