from main.models import SubscriptionPlan, SubscriptionSubPlan

mealtypes = ["BREAKFAST", "LUNCH", "DINNER", "TIFFIN_LUNCH", "EARLY_BREAKFAST"]
meal_combinations = [[meal] for meal in mealtypes] + [
    ["BREAKFAST", "LUNCH"],
    ["BREAKFAST", "DINNER"],
    ["LUNCH", "DINNER"],
    ["BREAKFAST", "LUNCH", "DINNER"],
    ["BREAKFAST", "TIFFIN_LUNCH"],
    ["TIFFIN_LUNCH", "DINNER"],
    ["EARLY_BREAKFAST", "DINNER"],
    ["BREAKFAST", "TIFFIN_LUNCH", "DINNER"],
]


def create(base_plan_id):
    subplans = []
    for index, combination in enumerate(meal_combinations, start=1):
        subplans.append({"plan": base_plan_id, "name": ", ".join(combination).title(), "available_mealtypes": ",".join(combination), "plan_price": 100.00, "order": index})
    print(subplans)
    for subplan_data in subplans:
        SubscriptionSubPlan.objects.create(
            plan_id=subplan_data["plan"],
            name=subplan_data["name"],
            available_mealtypes=subplan_data["available_mealtypes"],
            plan_price=subplan_data["plan_price"],
            order=subplan_data["order"],
        )
    print(f"{base_plan_id} created")


def run():
    for item in SubscriptionPlan.objects.all():
        create(item.id)
