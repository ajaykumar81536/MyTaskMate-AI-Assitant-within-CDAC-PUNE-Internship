# components/navbar.py
import reflex as rx

def navbar() -> rx.Component:
    nav_links = ["Dashboard", "Tasks"]
    return rx.hstack(
        rx.spacer(),
        rx.hstack(*[rx.link(name, href=f"/{name.lower()}", color="#64748b") for name in nav_links], spacing="5"),
        rx.avatar(src="/avatar.png", size="2"),
        align="center", spacing="6", width="100%", height="70px", padding="0 2em",
        border_bottom="1px solid #e2e8f0", background_color="white",
    )