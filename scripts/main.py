from main.models import Subscription


def run():
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        subscription.save()
