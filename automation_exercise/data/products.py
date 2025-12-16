from dataclasses import dataclass


@dataclass
class Product:
    name: str
    quantity: int = 1

    def reset_quantity(self) -> None:
        self.quantity = 1


product_men_tshirt: Product = Product("Men Tshirt")
product_women_blue_top: Product = Product("Blue Top")
