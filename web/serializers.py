from rest_framework import serializers

from main.models import MealPlan, SubscriptionPlan, SubscriptionSubPlan


class SubscriptionSubPlanSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.meals()

    class Meta:
        model = SubscriptionSubPlan
        fields = ["id", "name", "plan_price", "order"]


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    web_url = serializers.SerializerMethodField()
    sub_plans = SubscriptionSubPlanSerializer(source="subscriptionsubplan_set", many=True)

    def get_web_url(self, obj):
        return obj.get_web_url()

    class Meta:
        model = SubscriptionPlan
        fields = ["id", "validity", "order", "web_url", "sub_plans"]


class MealPlanSerializer(serializers.ModelSerializer):
    menu_item = serializers.SerializerMethodField()
    meal_category = serializers.SerializerMethodField()
    mealtype = serializers.SerializerMethodField()

    def get_menu_item(self, obj):
        return obj.menu_item.name

    def get_meal_category(self, obj):
        return obj.meal_category.name

    def get_mealtype(self, obj):
        return obj.menu_item.mealtype

    class Meta:
        model = MealPlan
        exclude = ["created", "updated", "is_active", "creator"]
