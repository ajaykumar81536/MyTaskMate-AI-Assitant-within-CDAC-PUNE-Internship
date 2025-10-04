# components/sidebar.py
import reflex as rx

def sidebar() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.icon(tag="bar_chart_horizontal", size=28),
            rx.heading("MyTaskMate", size="6"),
            align="center", spacing="2", padding_bottom="1.5em",
        ),
        rx.button("New Chat", size="3", width="100%", bg="#14b8a6", color="white"),
        align="start", width="280px", height="100vh", padding="1.5em",
        border_right="1px solid #e2e8f0", background_color="white",
        position="fixed", top="0", left="0",
    )