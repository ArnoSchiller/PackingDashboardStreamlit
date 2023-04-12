import json
from typing import List

from util.Product import Product


def load_products_from_json(file_path: str) -> List[Product]:
    products = []

    with open(file_path) as f:
        json_data = json.load(f)

        for p in json_data:
            products.append(Product.Schema().loads(json.dumps(p)))
        return products


"""
if __name__ == "__main__":
    import sys
    sys.path.append("..")
    print(load_products_from_json("src/config/products.json"))
"""
