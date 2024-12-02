from main.models import ItemMaster, MealCategory

data = [
    {"key": "cf77027a-07e9-4c64-82ac-f73a4cad7a77", "name": "Essential Flexitarian", "code": "EF "},
    {"key": "951454a5-69aa-405f-a8c7-01211ea0dbe6", "name": "Essential Pro Flexitarian", "code": "EPF"},
    {"key": "a23a42e4-85d3-4f31-bb74-1dfc1f80fd6b", "name": "Essential Vegetarian", "code": "EV"},
    {"key": "14bbf17e-4650-486f-8888-33abdcc47548", "name": "Regular Flexitarian", "code": "RF"},
    {"key": "034f2beb-8948-4366-b73d-d8d88d6227d8", "name": "Regular Non Vegetarian", "code": "RNV"},
    {"key": "77227fce-6f40-4592-a679-16b7510c52c3", "name": "Regular Vegetarian", "code": "RV"},
    {"key": "b250add2-f03d-46b1-a908-f945b7b72ef5", "name": "Deluxe Flexitarian", "code": "DF"},
    {"key": "c79ac7ee-d035-4be7-beda-f0958b36fa1c", "name": "Deluxe Non Vegetarian", "code": "DNV"},
    {"key": "614c04e6-ee81-47d2-86a3-3bbea8ef8077", "name": "Deluxe Vegetarian", "code": "DV"},
    {"key": "f9fe5731-6e81-4831-ac35-5afa1504f65a", "name": "Standard Flexitarian", "code": "SF"},
    {"key": "f1812e31-8e9b-42b0-8231-ef33b0bfaf78", "name": "Standard Non Vegetarian", "code": "SNV"},
    {"key": "2084fac6-d7d6-427c-9c9f-f779e7e4ffc9", "name": "Standard Vegetarian", "code": "SV"},
]


def run():
    for item in data:
        print(item["code"])
        items = ItemMaster.objects.filter(item_code__icontains=item["code"]).update(meal_category=MealCategory.objects.get(id=item["key"]))
