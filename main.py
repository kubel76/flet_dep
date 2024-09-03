import flet as ft
from tinydb import TinyDB, Query

# Ініціалізація БД
db = TinyDB("products_and_dash.json")
products_table = db.table('products')
dishes_table = db.table('dishes')


class EditDialog:
    def __init__(self, table, row_data, is_product, page, update_callback):
        self.table = table
        self.row_data = row_data
        self.is_product = is_product
        self.page = page
        self.update_callback = update_callback  # Колбек для оновлення списку

        if is_product:
            self.name_field = ft.TextField(
                value=row_data['name'], label="Назва продукту")
            self.calories_field = ft.TextField(
                value=row_data['calories'], label="Калорії/100г")
            self.proteins_field = ft.TextField(
                value=row_data['proteins'], label="Білки/100г")
            self.fat_field = ft.TextField(
                value=row_data['fat'], label="Жири/100г")
            self.carb_hyd_field = ft.TextField(
                value=row_data['carb_hyd'], label="Вуглеводи/100г")
        else:
            self.name_field = ft.TextField(
                value=row_data['name_dash'], label="Назва страви")
            self.calories_field = ft.TextField(
                value=row_data['total_calories'], label="Калорії/100г", disabled=True)
            self.proteins_field = ft.TextField(
                value=row_data['total_proteins'], label="Білки/100г", disabled=True)
            self.fat_field = ft.TextField(
                value=row_data['total_fat'], label="Жири/100г", disabled=True)
            self.carb_hyd_field = ft.TextField(
                value=row_data['total_carb_hyd'], label="Вуглеводи/100г", disabled=True)

            # Список всіх продуктів для вибору
            self.products = products_table.all()

            # Створюємо список чекбоксів для продуктів
            self.checkboxes = []
            self.selected_products = row_data.get('products', [])

            for product in self.products:
                checked = product['name'] in self.selected_products
                checkbox = ft.Checkbox(
                    label=product['name'], value=checked, on_change=self.update_ingredients)
                self.checkboxes.append(checkbox)

    def update_ingredients(self, e):
        # Оновлення вибраних продуктів
        self.selected_products = [cb.label for cb in self.checkboxes if cb.value]
        self.page.update()

    def open(self):
        def save_changes(e):
            if self.is_product:
                self.table.update({
                    'name': self.name_field.value,
                    'calories': self.calories_field.value,
                    'proteins': self.proteins_field.value,
                    'fat': self.fat_field.value,
                    'carb_hyd': self.carb_hyd_field.value},
                    Query().name == self.row_data['name'])
            else:
                self.table.update({
                    'name_dash': self.name_field.value,
                    'total_calories': self.calories_field.value,
                    'total_proteins': self.proteins_field.value,
                    'total_fat': self.fat_field.value,
                    'total_carb_hyd': self.carb_hyd_field.value,
                    'products': self.selected_products},
                    Query().name_dash == self.row_data['name_dash'])
            dialog.open = False
            self.update_callback()  # Виклик функції оновлення списку
            self.page.update()

        def delete_item(e):
            if self.is_product:
                self.table.remove(Query().name == self.row_data['name'])
            else:
                self.table.remove(Query().name_dash == self.row_data['name_dash'])
            dialog.open = False
            self.update_callback()  # Виклик функції оновлення списку
            self.page.update()

        def close_dialog(e):
            dialog.open = False
            self.update_callback()  # Виклик функції оновлення списку
            self.page.update()

        content_fields = [
            self.name_field,
            self.calories_field,
            self.proteins_field,
            self.fat_field,
            self.carb_hyd_field
        ]

        if not self.is_product:
            content_fields.append(ft.Text("Виберіть інгредієнти"))
            content_fields.extend(self.checkboxes)

        dialog = ft.AlertDialog(
            title=ft.Text(f"Редагування: {self.name_field.value}"),
            content=ft.Column(content_fields),
            actions=[
                ft.TextButton("Зберегти", on_click=save_changes),
                ft.TextButton("Видалити", on_click=delete_item),
                ft.TextButton("Закрити", on_click=close_dialog)
            ]
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()


def main(page: ft.Page):
    # Створення контейнера для даних
    data_container = ft.Column()

    def update_products():
        get_products(None)

    def update_dishes():
        get_dishes(None)

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
                            "Редагувати",
                            on_click=lambda e, row_data=row: EditDialog(products_table, row_data, True, page, update_products).open())
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
                            "Редагувати",
                            on_click=lambda e, row_data=row: EditDialog(dishes_table, row_data, False, page, update_dishes).open())
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
