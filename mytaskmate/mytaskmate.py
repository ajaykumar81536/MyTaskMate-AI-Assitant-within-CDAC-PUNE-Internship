# mytaskmate/mytaskmate.py
import reflex as rx
from core.state import AppState, ChatMessage
from components.sidebar import sidebar
from components.navbar import navbar
from components.dashboard import dashboard_page
from components.pages import tasks_page

def message_card(message: ChatMessage) -> rx.Component:
    is_user = message.role == "user"
    return rx.box(
        rx.markdown(message.content, component_map={"h3": rx.heading}),
        padding=rx.cond(message.bg_image, "1.5em", "1em"),
        border_radius="xl",
        background=rx.cond(
            message.bg_image,
            f"linear-gradient(rgba(0,0,0,0.2), rgba(0,0,0,0.2)), url({message.bg_image})",
            rx.cond(is_user, "#14b8a6", "#f1f5f9")
        ),
        color=rx.cond(is_user | message.bg_image, "white", "#0f172a"),
        align_self=rx.cond(is_user, "flex-end", "flex-start"),
        max_width="85%",
    )

def chat_input_bar() -> rx.Component:
    return rx.center(
        rx.hstack(
            rx.input(
                placeholder="Type your prompt here...",
                value=AppState.prompt_text,
                on_change=AppState.set_prompt_text,
                on_key_down=lambda k: rx.cond(k=="Enter", AppState.handle_send(), None),
                flex_grow=1, size="3", variant="soft",
            ),
            rx.upload(
                rx.button(rx.icon(tag="paperclip"), variant="soft"),
                on_drop=AppState.handle_upload(rx.upload_files()),
                border="0px", padding="0px", background="transparent",
            ),
            rx.button("Send", on_click=AppState.handle_send, is_loading=AppState.is_processing),
            align="center", spacing="4", width="100%",
        ),
        position="sticky", bottom="0", width="100%", padding="1em", background_color="rgba(255,255,255,0.8)",
    )

def main_layout(content: rx.Component) -> rx.Component:
    return rx.hstack(
        sidebar(),
        rx.vstack(
            navbar(),
            rx.box(content, padding="2em", width="100%", height="calc(100vh - 70px)", overflow_y="auto"),
            padding_left="280px", width="100%", height="100vh",
        ),
        align="start",
    )

@rx.page(route="/", on_load=AppState.on_load)
def index() -> rx.Component:
    return main_layout(
        rx.vstack(
            rx.box(
                rx.foreach(AppState.chat_history, message_card),
                display="flex", flex_direction="column", spacing="5",
                width="100%", max_width="900px", margin="auto", flex_grow=1,
            ),
            chat_input_bar(),
            height="100%", width="100%", overflow_y="auto",
        )
    )

@rx.page(route="/dashboard", on_load=AppState.on_load)
def dashboard() -> rx.Component: return main_layout(dashboard_page())

@rx.page(route="/tasks", on_load=AppState.on_load)
def tasks() -> rx.Component: return main_layout(tasks_page())

app = rx.App(theme=rx.theme(appearance="light", accent_color="teal"))