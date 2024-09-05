# controller.py
import flet as ft
import view
# import models


def start_page(page):
    page.controls.clear()
    page.add(
        ft.Text('Прога стоп жиртрест', size=18),
        ft.Divider(),
        ft.Row([
            ft.ElevatedButton("Перегляд продуктів",
                              on_click=lambda e: view.get_products(page)),
            ft.ElevatedButton("Перегляд страв",
                              on_click=lambda e: view.get_dishes(page)),
            # ft.Divider(),
        ])
    )
    page.update()
