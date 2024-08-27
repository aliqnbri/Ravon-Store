import json
from django.utils.text import slugify

import random
try:
    with open('fake_product_json.json', 'r') as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    exit(1)

# Transform the data into the desired format
transformed_data = [
    {
        "model": "product.product",
        "pk": item['pk'],
        "fields": {
            "created_at": "2024-08-06T12:20:05.372Z",
            "updated_at": "2024-08-06T18:09:21.603Z",
            "is_active": True,
            "name": item['name'],
            "slug": slugify(item['name']),
            "image": "media/products/iphone-15-pro-gray.jpg",
            "description": item['description'],
            "price":  item['price'],
            "discount": "0.00",
            "is_available": True,
            "brand": item['brand'],
            "available_quantity": random.randint(1, 99),
            "reviews": [],
            "category": [item['category']]
        }
    }
    for item in data]

# Write the transformed data to a new JSON file
with open('fake_product.json', 'w') as f:
    json.dump(transformed_data, f, indent=4)
