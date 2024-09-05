# main.py
import flet as ft
import controller


def main(page: ft.Page):
    controller.start_page(page)


ft.app(target=main)
