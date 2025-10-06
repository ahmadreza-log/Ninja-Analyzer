"""
Base page class to share common UI and helper utilities between pages.
"""

import flet as ft
from src.utils.datetime import now_formatted


class BasePage:
    def __init__(self):
        self.page: ft.Page | None = None

    def set_page(self, page: ft.Page) -> None:
        self.page = page

    def show_info(self, container: ft.Container, message: str) -> None:
        container.content.controls.clear()
        container.content.controls.append(
            ft.Text(message, size=16, color=ft.Colors.GREY_600, font_family="Iransans-Regular")
        )
        if self.page:
            self.page.update()

    def current_datetime(self) -> str:
        return now_formatted()


