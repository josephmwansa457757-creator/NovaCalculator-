# Splash screen - shows first, then the calculator opens
import flet as ft


def build_splash_screen(page, on_done):
    splash = ft.Container(
        content=ft.Column(
            [
                ft.Text("Nova Spark", size=52, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text("Founder, Joseph Mwansa and Zephaniah Mwansa", size=18, text_align=ft.TextAlign.CENTER),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        ),
        alignment=ft.Alignment.CENTER,
        expand=True,
    )

    page.add(splash)
    page.update()

    def show_calculator():
        page.controls.clear()
        page.update()
        on_done()

    # Show splash for 2.5 seconds, then open calculator
    import threading
    threading.Timer(2.5, show_calculator).start()
