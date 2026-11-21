# Builds the calculator screen
import re
import flet as ft
from function import add, subtract, multiply, divide


def build_calculator_ui(page):
    # One display for typing calculations AND showing the answer.
    display = ft.TextField(
        label="Enter a calculation",
        hint_text="Example: 25 + 15",
        value="",
        autofocus=True,
        text_size=28,
        on_submit=lambda e: calculate(),
    )
    error_text = ft.Text("", color=ft.Colors.RED, size=18)

    def calculate():
        expression = display.value.strip()
        match = re.fullmatch(
            r"(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)",
            expression,
        )
        if not match:
            error_text.value = "Enter a calculation like 25 + 15."
            page.update()
            return

        a = float(match.group(1))
        operator = match.group(2)
        b = float(match.group(3))

        if operator == "+":
            answer = add(a, b)
        elif operator == "-":
            answer = subtract(a, b)
        elif operator == "*":
            answer = multiply(a, b)
        else:
            answer = divide(a, b)

        if answer == "Error":
            error_text.value = "Cannot divide by zero."
            page.update()
            return

        if answer == int(answer):
            answer = int(answer)

        error_text.value = ""
        # The answer appears inside the SAME display.
        display.value = f"{expression} = {answer}"
        page.update()

    def press(key):
        current = display.value

        if key == "C":
            display.value = ""
            error_text.value = ""
        elif key == "⌫":
            display.value = "" if "=" in current else current[:-1]
            error_text.value = ""
        elif key == "=":
            calculate()
            return
        else:
            if "=" in current:
                if key.isdigit() or key == ".":
                    display.value = ""
                elif key in "+-*/":
                    display.value = current.split("=")[-1].strip()
            display.value += key
            error_text.value = ""

        page.update()

    # Buttons share the available row width, keeping them equal in size.
    def make_button(label):
        return ft.Button(
            content=label,
            on_click=lambda e: press(label),
            expand=1,
            height=button_height,
        )

    button_rows = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["C", "0", ".", "+"],
        ["⌫", "="],
    ]

    button_height = 76
    button_controls = []
    for row in button_rows:
        button_controls.append(
            ft.Row(
                [make_button(key) for key in row],
                spacing=12,
            )
        )

    title = ft.Text("Nova Calculator", size=34, weight=ft.FontWeight.BOLD)

    # This container grows with the window while keeping the calculator
    # at a comfortable maximum width on very large screens.
    calculator_column = ft.Column(
        [
            title,
            display,
            *button_controls,
            error_text,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        spacing=14,
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )

    calculator_container = ft.Container(
        content=calculator_column,
        padding=20,
        alignment=ft.Alignment.CENTER,
    )

    def resize_layout(e=None):
        window_width = page.width or 800
        window_height = page.height or 700

        # Use most of the available width, but avoid stretching too far
        # on very wide monitors.
        calculator_container.width = min(window_width * 0.94, 850)
        calculator_container.height = window_height

        # Button height follows the window height, within sensible limits.
        new_button_height = max(58, min(100, window_height * 0.105))
        for row in button_controls:
            for button in row.controls:
                button.height = new_button_height

        display.height = max(76, min(120, window_height * 0.14))
        display.text_size = max(22, min(34, window_width * 0.035))
        title.size = max(28, min(40, window_width * 0.045))

        page.update()

    page.on_resized = resize_layout
    page.add(
        ft.Row(
            [calculator_container],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )
    resize_layout()
