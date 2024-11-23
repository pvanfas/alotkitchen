from main.models import ItemMaster


def run():
    items = ItemMaster.objects.all().update(price=0.00)
