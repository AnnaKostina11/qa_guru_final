from dataclasses import dataclass


@dataclass
class Product:
    # Простая модель товара для UI-тестов (корзина/чекаут).
    # Хранит имя товара (как оно отображается на сайте) и количество.
    name: str
    quantity: int = 1

    def reset_quantity(self) -> None:
        # Сброс количества к дефолтному значению для переиспользования объекта в нескольких тестах.
        self.quantity = 1


# Предопределённые "константы" товаров, чтобы не дублировать строки в тестах.
product_men_tshirt: Product = Product("Men Tshirt")
product_women_blue_top: Product = Product("Blue Top")
