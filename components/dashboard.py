# components/dashboard.py
import reflex as rx
from core.state import AppState

def stat_card(label: str, value: rx.Var[str | int]) -> rx.Component:
    return rx.card(rx.vstack(rx.text(label, size="3"), rx.heading(value, size="7"), spacing="1"))

def dashboard_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Dashboard", size="8"),
        rx.hstack(
            stat_card("Total Tasks", AppState.tasks.length()),
            stat_card("Completed", AppState.completed_tasks_count),
            stat_card("Pending", AppState.pending_tasks_count),
            spacing="5", width="100%",
        ),
        rx.heading("Upcoming Tasks", size="6", margin_top="2em"),
        rx.card(
            rx.cond(
                AppState.pending_tasks_list.length() > 0,
                rx.ordered_list(
                    rx.foreach(AppState.pending_tasks_list, lambda task: rx.list_item(task.description)),
                    spacing="2",
                ),
                rx.text("No pending tasks. Well done!"),
            )
        ),
        width="100%", max_width="900px", align="start", spacing="5",
    )