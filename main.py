import flet as ft
from tinydb import TinyDB

# Ініціалізація БД
db = TinyDB("products_and_dash.json")
products_table = db.table('products')
dishes_table = db.table('dishes')


def main(page: ft.Page):
    # Створення контейнера для даних
    data_container = ft.Column()

    def open_edit_dialog(row_data):
        # Функція для відкриття діалогового вікна редагування
        def save_changes(e):
            # Зберігайте зміни тут
            print(f"Saving changes for: {row_data['name']}")
            dialog.close()
            page.update()

        def delete_product(e):
            # Видалення продукту
            print(f"Deleting product: {row_data['name']}")
            dialog.close()
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text(f"Редагування продукту: {row_data['name']}"),
            content=ft.Column([
                ft.TextField(value=row_data['name'], label="Назва продукту"),
                ft.TextField(value=row_data['calories'], label="Калорії/100г"),
                ft.TextField(value=row_data['proteins'], label="Білки/100г"),
                ft.TextField(value=row_data['fat'], label="Жири/100г"),
                ft.TextField(
                    value=row_data['carb_hyd'], label="Вуглеводи/100г")
            ]),
            actions=[
                ft.TextButton("Зберегти", on_click=save_changes),
                ft.TextButton("Видалити", on_click=delete_product),
                ft.TextButton("Закрити", on_click=lambda e: dialog.close())
            ]
        )
        page.dialog = dialog
        dialog.open()

    def get_products(e):
        # Очищення контейнера для даних
        data_container.controls.clear()

        # Додавання нових елементів до контейнера
        data_container.controls.append(ft.Divider())
        data_container.controls.append(ft.Text('Продукти в базі', size=18))
        data_container.controls.append(ft.Divider())

        products = products_table.all()

        # Оголошення стовпців таблиці
        columns = [
            ft.DataColumn(ft.Text('Продукт')),
            ft.DataColumn(ft.Text('Ккал/100г')),
            ft.DataColumn(ft.Text('Білки/100г')),
            ft.DataColumn(ft.Text('Жири/100г')),
            ft.DataColumn(ft.Text('Вуглеводи/100г')),
            ft.DataColumn(ft.Text('Дії'))  # Додано стовпець для кнопок
        ]

        # Створення рядків таблиці
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(row['name'])),
                    ft.DataCell(ft.Text(row['calories'])),
                    ft.DataCell(ft.Text(row['proteins'])),
                    ft.DataCell(ft.Text(row['fat'])),
                    ft.DataCell(ft.Text(row['carb_hyd'])),
                    ft.DataCell(ft.Row([
                        ft.ElevatedButton(
                            "Редагувати", on_click=lambda e, row_data=row: open_edit_dialog(row_data))
                    ]))
                ]
            )
            for row in products
        ]

        # Додавання таблиці на контейнер
        data_container.controls.append(
            ft.DataTable(columns=columns, rows=rows))
        data_container.controls.append(ft.Divider())

        # Оновлення сторінки
        page.update()

    def get_dishes(e):
        # Очищення контейнера для даних
        data_container.controls.clear()

        # Додавання нових елементів до контейнера
        data_container.controls.append(ft.Divider())
        data_container.controls.append(ft.Text('Страви в базі', size=18))
        data_container.controls.append(ft.Divider())

        dishes = dishes_table.all()

        # Оголошення стовпців таблиці
        columns = [
            ft.DataColumn(ft.Text('Страва')),
            ft.DataColumn(ft.Text('Ккал')),
            ft.DataColumn(ft.Text('Білки')),
            ft.DataColumn(ft.Text('Жири')),
            ft.DataColumn(ft.Text('Вуглеводи')),
            ft.DataColumn(ft.Text('Склад')),
            ft.DataColumn(ft.Text('Дії'))  # Додано стовпець для кнопок
        ]

        # Створення рядків таблиці
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(row['name_dash'])),
                    ft.DataCell(ft.Text(row['total_calories'])),
                    ft.DataCell(ft.Text(row['total_proteins'])),
                    ft.DataCell(ft.Text(row['total_fat'])),
                    ft.DataCell(ft.Text(row['total_carb_hyd'])),
                    ft.DataCell(ft.Text(", ".join(row['products']))),
                    ft.DataCell(ft.Row([
                        ft.ElevatedButton(
                            "Редагувати", on_click=lambda e, row_data=row: open_edit_dialog(row_data))
                    ]))
                ]
            )
            for row in dishes
        ]

        # Додавання таблиці на контейнер
        data_container.controls.append(
            ft.DataTable(columns=columns, rows=rows))
        data_container.controls.append(ft.Divider())

        # Оновлення сторінки
        page.update()

    # Додавання кнопок і контейнера на сторінку
    page.add(ft.Column([
        ft.Row([
            ft.ElevatedButton('Список продуктів', on_click=get_products),
            ft.ElevatedButton('Список страв', on_click=get_dishes)
        ]),
        data_container
    ]))


ft.app(target=main)
