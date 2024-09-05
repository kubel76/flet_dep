# models.py
from tinydb import TinyDB
import flet as ft

# Ініціалізація БД
db = TinyDB("products_and_dash.json")
products_table = db.table('products')
dishes_table = db.table('dishes')
menu_table = db.table('menu')


def add_to_products(name: str, calories: float, proteins:
                    float, fat: float, carb_hyd: float):
    products_table.insert(
        {
            "name": name,
            "calories": calories,
            "proteins": proteins,
            "fat": fat,
            "carb_hyd": carb_hyd,
        }
    )


def add_to_dish(page, product):
    # Показуємо повідомлення про те, який продукт додається до страви
    page.dialog = ft.AlertDialog(
        title=ft.Text(f"Додаємо продукт: {product['name']} до страви"),
        on_dismiss=lambda e: print("Додавання завершено"),
    )
    page.dialog.open = True
    page.update()


def edit_product(page, product):
    # Показуємо повідомлення про те, який продукт редагується
    page.dialog = ft.AlertDialog(
        title=ft.Text(f"Редагуємо продукт: {product['name']}"),
        on_dismiss=lambda e: print("Редагування завершено"),
    )
    page.dialog.open = True
    page.update()


def delete_product(page, product):
    # Видаляємо продукт з бази
    page.dialog = ft.AlertDialog(
        title=ft.Text(f"Видаляємо продукт: {product['name']} до страви"),
        on_dismiss=lambda e: print("Видалення завершено"),
    )
    page.dialog.open = True
    page.update()
