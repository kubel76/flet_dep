# view.py
import flet as ft
import models
import controller

table_settings = {
    "bgcolor": "yellow",
    "border": ft.border.all(2, "red"),
    "border_radius": 10,
    "vertical_lines": ft.BorderSide(3, "blue"),
    "horizontal_lines": ft.BorderSide(1, "green"),
    "sort_column_index": 0,
    "sort_ascending": True,
    "heading_row_color": ft.colors.BLACK12,
    "data_row_color": {ft.ControlState.HOVERED: "0x30FF0000"},
    "divider_thickness": 0
}


def get_products(page):
    search_field = ft.TextField(label='Назва продукту')
    success_message = ft.Text("", color="green")
    # Отримання продуктів з бази
    products = models.products_table.all()

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
                        on_click=lambda e, row_data=row: models.edit_product(
                            page, row_data)
                    ),
                    ft.ElevatedButton(
                        "Додати до страви",
                        on_click=lambda e, row_data=row: models.add_to_dish(
                            page, row_data)
                    ),
                    ft.ElevatedButton(
                        "Видалити",
                        on_click=lambda e, row_data=row: models.delete_product(
                            page, row_data)
                    ),
                ])),
            ],
        )
        for row in products
    ]

    # Додавання таблиці "Продукти" на сторінку з прокруткою
    page.controls.clear()
    page.add(
        ft.Row([
            ft.ElevatedButton(
                "На головну", on_click=lambda e: controller.start_page(page)),
            ft.ElevatedButton("Додати новий продукт",
                              on_click=lambda e: add_product_view(page)),
        ]),
        ft.Column([
            ft.Row([
                ft.Text('Продукти в базі', size=18),
                search_field,
                # ft.ElevatedButton("Пошук", on_click=lambda e: print(
                #     f'Шукаємо {search_field.value}'))
                ft.ElevatedButton("Пошук", on_click=lambda e: [
                                  # Виводимо повідомлення про успішне додавання
                                  setattr(success_message, 'value',
                                          f"Колись ми тут знайдемо продукт {search_field.value}"),
                                  # Очищуємо всі поля
                                  setattr(search_field, 'value', ""),
                                  page.update(),
                                  ]
                                  ),
                success_message
            ]),
            ft.Divider(),
            # Додаємо прокрутку до таблиці через ft.Column з параметром scroll
            ft.Column(
                [
                    ft.DataTable(
                        **table_settings,
                        columns=columns,
                        rows=rows,
                    ),
                ],
                height=400,  # Встановлюємо висоту контейнера
                scroll="auto"  # Додаємо прокрутку
            ),
            ft.Divider(),
        ]),
    )
    page.update()


def get_dishes(page):
    dishes = models.dishes_table.all()

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
                        on_click=lambda e, row_data=row: models.edit_dish)
                ]))
            ]
        )
        for row in dishes
    ]

    # Додавання таблиці "Страви" на сторінку
    page.controls.clear()
    page.add(
        ft.Row([
            ft.ElevatedButton(
                "На головну", on_click=lambda e: controller.start_page(page)),
            ft.ElevatedButton("Додати нову ставу",
                              on_click=lambda e: print("Додаємо страву")),
        ]),
        ft.Column([
            ft.Text('Страви в базі', size=18),
            ft.Divider(),
            ft.DataTable(**table_settings, columns=columns, rows=rows),
            ft.Divider(),
        ])
    )
    page.update()


def add_product_view(page):
    # Створюємо текстові поля і зберігаємо їх у змінні
    name_field = ft.TextField(label='Назва продукта', max_length=50)
    calories_field = ft.TextField(label='Ккалорії (кал)', max_length=10)
    proteins_field = ft.TextField(label='Білки (грами)', max_length=10)
    fat_field = ft.TextField(label='Жири (грами)', max_length=10)
    carb_hyd_field = ft.TextField(label='Вуглеводи (грами)', max_length=10)

    # Текст для повідомлення про успішне додавання
    success_message = ft.Text("", color="green")

    page.controls.clear()
    page.add(
        ft.Row([
            ft.ElevatedButton(
                "На головну", on_click=lambda e: controller.start_page(page)),
            ft.ElevatedButton("Назад", on_click=lambda e: get_products(page)),
        ]),
        ft.Column([
            ft.Text('Додавання нового продукта', size=18),
            ft.Divider(),
            name_field,
            calories_field,
            proteins_field,
            fat_field,
            carb_hyd_field,
            ft.ElevatedButton(
                "Додати",
                # Лямбда-функція з логікою додавання продукту, очищенням полів та виведенням повідомлення
                on_click=lambda e: [
                    models.add_to_products(
                        name=name_field.value,
                        calories=float(calories_field.value),
                        proteins=float(proteins_field.value),
                        fat=float(fat_field.value),
                        carb_hyd=float(carb_hyd_field.value),
                    ),
                    # Виводимо повідомлення про успішне додавання
                    setattr(success_message, 'value',
                            f"Продукт {name_field.value} успішно додано!"),
                    # Очищуємо всі поля
                    setattr(name_field, 'value', ""),
                    setattr(calories_field, 'value', ""),
                    setattr(proteins_field, 'value', ""),
                    setattr(fat_field, 'value', ""),
                    setattr(carb_hyd_field, 'value', ""),
                    # Оновлюємо сторінку
                    page.update()
                ]
            ),
            success_message  # Поле для виведення повідомлення
        ]),
    )
    page.update()
