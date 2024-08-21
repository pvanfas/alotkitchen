from django import template

from main.models import SubscriptionPlan

register = template.Library()


@register.simple_tag
def get_price(group, validity):
    if SubscriptionPlan.objects.filter(group=group, validity=validity).exists():
        plans = SubscriptionPlan.objects.filter(group=group, validity=validity)
        return plans.first().plan_price
    else:
        return 0


@register.simple_tag
def get_plan_link(group, validity):
    if SubscriptionPlan.objects.filter(group=group, validity=validity).exists():
        plans = SubscriptionPlan.objects.filter(group=group, validity=validity)
        return plans.first().get_absolute_url()
    else:
        return "javascript:void(0);"
