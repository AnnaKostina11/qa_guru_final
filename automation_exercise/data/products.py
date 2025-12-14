class Product:
    def __init__(self, name, quantity=1):
        self.name = name
        self.quantity = quantity
    def reset_quantity(self):
        self.quantity = 1

product_men_tshirt = Product("Men Tshirt")
product_women_blue_top = Product("Blue Top")