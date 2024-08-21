from main.models import Combo


def run():
    qs = Combo.objects.all()
    for q in qs:
        if q.available_weeks == None:
            print(q.available_weeks)
