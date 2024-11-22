from rest_framework import serializers

from main.models import SubscriptionPlan, SubscriptionSubPlan


class SubscriptionSubPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionSubPlan
        fields = ["id", "name", "plan_price", "order"]


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    sub_plans = SubscriptionSubPlanSerializer(source="subscriptionsubplan_set", many=True)

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    class Meta:
        model = SubscriptionPlan
        fields = ["id", "name", "validity", "order", "absolute_url", "sub_plans"]
