# Starts the Nova Calculator app
import flet as ft
from splash import build_splash_screen
from ui import build_calculator_ui


def main(page: ft.Page):
    page.title = "Nova Calculator"
    page.padding = 8
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.expand = True
    build_splash_screen(page, lambda: build_calculator_ui(page))


ft.run(main)
