from tinydb import TinyDB, Query
import re

# Ініціалізація БД
db = TinyDB("products_and_dash.json")
products_table = db.table('products')
dishes_table = db.table('dishes')


# Функція додавання запису до БД "Продукти"
def add_product(name: str, calories: int, proteins: float, fat: float, carb_hyd: float):
    products_table.insert(
        {
            "name": name,
            "calories": calories,
            "proteins": proteins,
            "fat": fat,
            "carb_hyd": carb_hyd,
        }
    )
    print(f'Продукт "{name}" доданий у БД.')


# Функція перегляду всіх записів БД "Продукти"
def view_products():
    products = products_table.all()
    if products:
        for product in products:
            print(
                f'Продукт: {product["name"]}, Калорійність/100г: {product["calories"]}, Білки: {product["proteins"]}, Жири: {product["fat"]}, Вуглеводи: {product["carb_hyd"]}'
            )
    else:
        print("БД пуста.")


# Функція видалення продукту
def delete_product(name: str):
    product = Query()
    result = products_table.remove(product.name == name)
    if result:
        print(f'Продукт "{name}" видалено з БД.')
    else:
        print(f'Продукт "{name}" не знайдено.')


# Функція пошуку продуту
def search_prod(name: str) -> str:
    product = Query()
    # Використовуємо регулярний вираз для пошуку часткових збігів
    pattern = f'.*{re.escape(name)}.*'
    result = products_table.search(
        product.name.matches(pattern, flags=re.IGNORECASE))

    if result:
        # Формуємо список знайдених продуктів
        found_products = []
        for res in result:
            product_info = f'Продукт: {res["name"]}, Калорійність/100г: {res["calories"]}, Білки: {res["proteins"]}, Жири: {res["fat"]}, Вуглеводи: {res["carb_hyd"]}'
            found_products.append(product_info)

        # Повертаємо всі знайдені продукти
        return "\n".join(found_products)
    else:
        return f'Продукт "{name}" не знайдено.'


# Функція додавання страви
def add_dash(name: str, products: list) -> None:
    total_calories = sum(product["calories"] for product in products)
    total_proteins = sum(product["proteins"] for product in products)
    total_fat = sum(product["fat"] for product in products)
    total_carb_hyd = sum(product["carb_hyd"] for product in products)

    dishes_table.insert(
        {
            "name_dash": name,
            "products": [product["name"] for product in products],
            "total_calories": total_calories,
            "total_proteins": total_proteins,
            "total_fat": total_fat,
            "total_carb_hyd": total_carb_hyd,
        }
    )
    print(f'Страва "{name}" додана у БД.')


# Функція перегляду страв
def view_dashes():
    dashes = dishes_table.all()
    if dashes:
        for dash in dashes:
            print(
                f'Страва: {dash["name_dash"]}, Калорійність: {dash["total_calories"]}, Білки: {dash["total_proteins"]}, Жири: {dash["total_fat"]}, Вуглеводи: {dash["total_carb_hyd"]}'
            )
            print(f'Склад: {", ".join(dash["products"])}')
    else:
        print("Немає страв у БД.")


# Функція видалення страви
def delete_dash(name: str):
    dash = Query()
    result = dishes_table.remove(dash.name_dash == name)
    if result:
        print(f'Страва "{name}" видалена з БД.')
    else:
        print(f'Страва "{name}" не знайдена.')


# Функція пошуку страви

def search_dash(name: str) -> str:
    dash = Query()
    # Використовуємо регулярний вираз для пошуку часткових збігів
    pattern = f'.*{re.escape(name)}.*'
    result = dishes_table.search(
        dash.name_dash.matches(pattern, flags=re.IGNORECASE))
    if result:
        # Формуємо список знайдених страв
        found_dashes = []
        for res in result:
            dash_info = f'Страва: {res["name_dash"]}, Калорійність: {res["total_calories"]}, Білки: {res["total_proteins"]}, Жири: {res["total_fat"]}, Вуглеводи: {res["total_carb_hyd"]}'
            found_dashes.append(dash_info)
        # Повертаємо всі знайдені страви
        return "\n".join(found_dashes)
    else:
        return f'Страва "{name}" не знайдена.'


# Інтерактивне меню
def menu():
    while True:
        print("\nМеню:")
        print("1. Додати продукт")
        print("2. Переглянути всі продукти")
        print("3. Видалити продукт")
        print("4. Додати страву")
        print("5. Переглянути страви")
        print("6. Видалити страву")
        print("7. Пошук продукту")
        print("8. Пошук страви")
        print("0. Вихід")
        choice = input("Виберіть дію: ")

        if choice == "1":
            name = input("Введіть назву продукта: ")
            calories = float(input("Введіть калорійність/100г: "))
            proteins = float(input("Введіть білки: "))
            fat = float(input("Введіть жири: "))
            carb_hyd = float(input("Введіть вуглеводи: "))
            add_product(name, calories, proteins, fat, carb_hyd)
        elif choice == "2":
            view_products()
        elif choice == "3":
            name = input("Введіть назву продукта для видалення: ")
            delete_product(name)
        elif choice == "4":
            name = input("Введіть назву страви: ")
            products = []
            while True:
                product_name = input(
                    "Введіть назву продукта (Enter без назви -> Вихід): ")
                if not product_name:
                    break
                product = Query()
                found_product = products_table.search(
                    product.name == product_name)
                if found_product:
                    products.append(found_product[0])
                else:
                    print(f'Продукт "{product_name}" не знайдено.')
                    continue
            add_dash(name, products)
        elif choice == "5":
            view_dashes()
        elif choice == "6":
            name = input("Введіть назву страви для видалення: ")
            delete_dash(name)
        elif choice == "7":
            name = input("Введіть назву продукту для пошуку: ")
            print(search_prod(name))
        elif choice == "8":
            name = input("Введіть назву страви для пошуку: ")
            print(search_dash(name))
        elif choice == "0":
            print("Завершення роботи.")
            break
        else:
            print("Невірний вибір. Спробуйте знову.")



