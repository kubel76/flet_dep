import flet as ft


class SwithThemeButton(ft.ElevatedButton):
    def __init__(self, text, on_click):
        super().__init__()
        self.text = text
        self.bgcolor = ft.colors.ORANGE_300
        self.color = ft.colors.BLUE_800
        self.on_click = on_click


def main(page: ft.Page):
    # Стандартна тема
    page.theme_mode = ft.ThemeMode.LIGHT

    # Функція перемикання теми
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()  # Оновлюємо сторінку після зміни теми

    # Додаємо кнопку перемикання теми
    switch_theme_button = SwithThemeButton(
        text="Перемкнути тему", on_click=toggle_theme)
    page.add(switch_theme_button)


ft.app(target=main)
