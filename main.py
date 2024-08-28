import flet as ft
from tinydb import TinyDB, Query

# Ініціалізація БД
db = TinyDB("products_and_dash.json")
products_table = db.table('products')
dishes_table = db.table('dishes')


def main(page: ft.Page):
    # Створення контейнера для даних
    data_container = ft.Column()

    def open_edit_dialog(row_data):
        # Функція для відкриття діалогового вікна редагування
        name_field = ft.TextField(value=row_data['name'], label="Назва продукту")
        calories_field = ft.TextField(value=row_data['calories'], label="Калорії/100г")
        proteins_field = ft.TextField(value=row_data['proteins'], label="Білки/100г")
        fat_field = ft.TextField(value=row_data['fat'], label="Жири/100г")
        carb_hyd_field = ft.TextField(value=row_data['carb_hyd'], label="Вуглеводи/100г")

        def save_changes(e):
            # Зберігання змін у БД
            products_table.update({'name': name_field.value, 
                                   'calories': calories_field.value, 
                                   'proteins': proteins_field.value, 
                                   'fat': fat_field.value, 
                                   'carb_hyd': carb_hyd_field.value}, 
                                  Query().name == row_data['name'])
            dialog.open = False
            page.update()
            get_products(e)  # Оновлюємо список продуктів

        def delete_product(e):
            # Видалення продукту
            products_table.remove(Query().name == row_data['name'])
            dialog.open = False
            page.update()
            get_products(e)  # Оновлюємо список продуктів

        def close_dialog(e):
            dialog.open = False
            page.update()  # Оновлення сторінки після закриття діалогу

        dialog = ft.AlertDialog(
            title=ft.Text(f"Редагування продукту: {row_data['name']}"),
            content=ft.Column([
                name_field,
                calories_field,
                proteins_field,
                fat_field,
                carb_hyd_field,
            ]),
            actions=[
                ft.TextButton("Зберегти", on_click=save_changes),
                ft.TextButton("Видалити", on_click=delete_product),
                ft.TextButton("Закрити", on_click=close_dialog)
            ]
        )

        # Додавання діалогу до overlay сторінки
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

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
