from scaffold.products.product import Product


class Builder:
    def __init__(self):
        self.product = None
        self.reset()

    def reset(self) -> None:
        self.product = Product()
