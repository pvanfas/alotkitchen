from main.models import Combo


def run():
    Combo.objects.all().update(price=0)
