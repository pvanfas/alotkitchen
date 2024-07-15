from django import template
from main.models import SubscriptionPlan

register = template.Library()

@register.simple_tag
def get_price(group, validity, price_type, plantype):
    print("price_type", price_type,"validity", validity,"group", group)
    if SubscriptionPlan.objects.filter(group=group, validity=validity, plantype=plantype).exists():
        plans = SubscriptionPlan.objects.filter(group=group, validity=validity, plantype=plantype)
        if price_type == "regular_price":
            return plans.first().regular_price
        elif price_type == "first_order_price":
            return plans.first().first_order_price
        elif price_type == "offer_price":
            return plans.first().offer_price
        else:
            return 0
    else:
        return 0
