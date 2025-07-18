from django.db import models
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from main.base import BaseModel

from .choices import BREAKFAST_DELIVERY_CHOICES, DAY_CHOICES, DINNER_DELIVERY_CHOICES, GROUP_CHOICES, LANGUAGE_CHOICES, LUNCH_DELIVERY_CHOICES, MEALTYPE_CHOICES, ORDER_STATUS_CHOICES


def get_week_number(date):
    day_of_month = date.day
    week_number = (day_of_month - 1) // 7 + 1
    return 2 if week_number % 2 == 0 else 1


class Branch(BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")

    def get_absolute_url(self):
        return reverse_lazy("main:branch_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("main:branch_list")

    def __str__(self):
        return str(self.name)


class Area(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    delivery_staffs = models.ManyToManyField("users.CustomUser", related_name="delivery_areas", limit_choices_to={"usertype": "Delivery"}, blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def __str__(self):
        return self.name


class MealCategory(BaseModel):
    order = models.PositiveIntegerField(default=1)
    group = models.CharField(max_length=200, choices=GROUP_CHOICES)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to="mealcategories/image")
    description = models.TextField(blank=True, null=True)
    brochure = models.FileField(upload_to="mealcategories/brochure/", blank=True, null=True)

    class Meta:
        ordering = ("order",)
        verbose_name = _("Meal Category")
        verbose_name_plural = _("Meal Categories")

    def get_plans(self):
        return SubscriptionPlan.objects.filter(is_active=True, meal_category=self)

    def api_url(self):
        return reverse_lazy("web:getplans_api", kwargs={"pk": self.pk})

    def menu_api_url(self):
        return reverse_lazy("web:getmeals_api", kwargs={"pk": self.pk})

    def get_web_url(self):
        return reverse_lazy("web:select_plan", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class SubscriptionPlan(BaseModel):
    meal_category = models.ForeignKey(MealCategory, on_delete=models.CASCADE)
    validity = models.PositiveIntegerField(help_text="In Days")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ("meal_category", "validity", "order")
        verbose_name = _("Subscription Plan")
        verbose_name_plural = _("Subscription Plans")

    def get_subs(self):
        return SubscriptionSubPlan.objects.filter(is_active=True, plan=self)

    @property
    def subplans_count(self):
        return self.get_subs().count()

    def get_web_url(self):
        return reverse_lazy("web:select_meals", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.meal_category} - {self.validity} Days"


class SubscriptionSubPlan(BaseModel):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    available_mealtypes = MultiSelectField(max_length=200, choices=MEALTYPE_CHOICES)
    plan_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ("order",)
        verbose_name = _("Sub Plan")
        verbose_name_plural = _("Sub Plans")

    def meals(self):
        mealtype_dict = dict(MEALTYPE_CHOICES)
        selected_mealtypes = [mealtype_dict[meal] for meal in self.available_mealtypes if meal in mealtype_dict]
        return ", ".join(selected_mealtypes)

    def get_web_url(self):
        return reverse_lazy("web:customize_meals", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.plan} - {self.meals()}"


class ItemCategory(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Item Category")
        verbose_name_plural = _("Item Categories")

    def __str__(self):
        return self.name


class ItemMaster(BaseModel):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="items")
    image = models.ImageField(upload_to="items/images/", blank=True, null=True)
    item_code = models.CharField(max_length=200, unique=True)
    mealtype = models.CharField(max_length=200, choices=MEALTYPE_CHOICES, blank=True, null=True)
    meal_category = models.ForeignKey(MealCategory, on_delete=models.CASCADE, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    is_veg = models.BooleanField(default=True)
    is_fallback = models.BooleanField(default=False)

    class Meta:
        ordering = ("item_code",)
        verbose_name = _("Item Master")
        verbose_name_plural = _("Item Masters")

    def get_absolute_url(self):
        return reverse_lazy("main:item_detail", kwargs={"pk": self.pk})

    def get_item_name(self):
        return ", ".join(item.name for item in self.items.all())

    def save(self, *args, **kwargs):
        if not self.pk:
            self.name = "Unnamed ItemMaster"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_code}: {self.name}" if not self.is_fallback else self.name


class MealPlan(BaseModel):
    meal_category = models.ForeignKey(MealCategory, on_delete=models.CASCADE, related_name="items")
    day = models.CharField(max_length=200, choices=DAY_CHOICES)
    menu_item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, blank=True, null=True)
    is_fallback = models.BooleanField(default=False, help_text="Day will be ignored for Fallback items (No Meal)")

    class Meta:
        ordering = ("meal_category", "day")
        verbose_name = _("Meal Plan")
        verbose_name_plural = _("Meal Plans")

    def __str__(self):
        # return f"{self.meal_category}: {self.day}}"
        return str(self.menu_item)


def get_lcqs(mealtype, day):
    return Q(menu_item__mealtype=mealtype, day=day) | Q(is_fallback=True)


class Preference(BaseModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="preferences", blank=True, null=True)
    session_id = models.CharField(max_length=200, blank=True, null=True)
    subscription_subplan = models.ForeignKey(SubscriptionSubPlan, on_delete=models.CASCADE, related_name="preferences", blank=True, null=True)

    monday_early_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="monday_early_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("EARLY_BREAKFAST", "Monday"))
    monday_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="monday_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("BREAKFAST", "Monday"))
    monday_tiffin_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="monday_tiffin_lunch", blank=True, null=True, limit_choices_to=get_lcqs("TIFFIN_LUNCH", "Monday"))
    monday_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="monday_lunch", blank=True, null=True, limit_choices_to=get_lcqs("LUNCH", "Monday"))
    monday_dinner = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="monday_dinner", blank=True, null=True, limit_choices_to=get_lcqs("DINNER", "Monday"))

    tuesday_early_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="tuesday_early_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("EARLY_BREAKFAST", "Tuesday"))
    tuesday_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="tuesday_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("BREAKFAST", "Tuesday"))
    tuesday_tiffin_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="tuesday_tiffin_lunch", blank=True, null=True, limit_choices_to=get_lcqs("TIFFIN_LUNCH", "Tuesday"))
    tuesday_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="tuesday_lunch", blank=True, null=True, limit_choices_to=get_lcqs("LUNCH", "Tuesday"))
    tuesday_dinner = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="tuesday_dinner", blank=True, null=True, limit_choices_to=get_lcqs("DINNER", "Tuesday"))

    wednesday_early_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="wednesday_early_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("EARLY_BREAKFAST", "Wednesday"))
    wednesday_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="wednesday_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("BREAKFAST", "Wednesday"))
    wednesday_tiffin_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="wednesday_tiffin_lunch", blank=True, null=True, limit_choices_to=get_lcqs("TIFFIN_LUNCH", "Wednesday"))
    wednesday_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="wednesday_lunch", blank=True, null=True, limit_choices_to=get_lcqs("LUNCH", "Wednesday"))
    wednesday_dinner = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="wednesday_dinner", blank=True, null=True, limit_choices_to=get_lcqs("DINNER", "Wednesday"))

    thursday_early_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="thursday_early_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("EARLY_BREAKFAST", "Thursday"))
    thursday_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="thursday_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("BREAKFAST", "Thursday"))
    thursday_tiffin_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="thursday_tiffin_lunch", blank=True, null=True, limit_choices_to=get_lcqs("TIFFIN_LUNCH", "Thursday"))
    thursday_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="thursday_lunch", blank=True, null=True, limit_choices_to=get_lcqs("LUNCH", "Thursday"))
    thursday_dinner = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="thursday_dinner", blank=True, null=True, limit_choices_to=get_lcqs("DINNER", "Thursday"))

    friday_early_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="friday_early_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("EARLY_BREAKFAST", "Friday"))
    friday_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="friday_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("BREAKFAST", "Friday"))
    friday_tiffin_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="friday_tiffin_lunch", blank=True, null=True, limit_choices_to=get_lcqs("TIFFIN_LUNCH", "Friday"))
    friday_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="friday_lunch", blank=True, null=True, limit_choices_to=get_lcqs("LUNCH", "Friday"))
    friday_dinner = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="friday_dinner", blank=True, null=True, limit_choices_to=get_lcqs("DINNER", "Friday"))

    saturday_early_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="saturday_early_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("EARLY_BREAKFAST", "Saturday"))
    saturday_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="saturday_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("BREAKFAST", "Saturday"))
    saturday_tiffin_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="saturday_tiffin_lunch", blank=True, null=True, limit_choices_to=get_lcqs("TIFFIN_LUNCH", "Saturday"))
    saturday_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="saturday_lunch", blank=True, null=True, limit_choices_to=get_lcqs("LUNCH", "Saturday"))
    saturday_dinner = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="saturday_dinner", blank=True, null=True, limit_choices_to=get_lcqs("DINNER", "Saturday"))

    sunday_early_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="sunday_early_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("EARLY_BREAKFAST", "Sunday"))
    sunday_breakfast = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="sunday_breakfast", blank=True, null=True, limit_choices_to=get_lcqs("BREAKFAST", "Sunday"))
    sunday_tiffin_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="sunday_tiffin_lunch", blank=True, null=True, limit_choices_to=get_lcqs("TIFFIN_LUNCH", "Sunday"))
    sunday_lunch = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="sunday_lunch", blank=True, null=True, limit_choices_to=get_lcqs("LUNCH", "Sunday"))
    sunday_dinner = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name="sunday_dinner", blank=True, null=True, limit_choices_to=get_lcqs("DINNER", "Sunday"))

    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    preferred_language = models.CharField(max_length=200, blank=True, null=True, choices=LANGUAGE_CHOICES)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    alternate_mobile = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    start_date = models.DateField("Subscription Starts from", blank=True, null=True)

    early_breakfast_address = models.ForeignKey("DeliveryAddress", on_delete=models.CASCADE, related_name="early_breakfast_address", blank=True, null=True)
    breakfast_address = models.ForeignKey("DeliveryAddress", on_delete=models.CASCADE, related_name="breakfast_address", blank=True, null=True)
    tiffin_lunch_address = models.ForeignKey("DeliveryAddress", on_delete=models.CASCADE, related_name="tiffin_lunch_address", blank=True, null=True)
    lunch_address = models.ForeignKey("DeliveryAddress", on_delete=models.CASCADE, related_name="lunch_address", blank=True, null=True)
    dinner_address = models.ForeignKey("DeliveryAddress", on_delete=models.CASCADE, related_name="dinner_address", blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=200, default="PENDING", choices=(("PENDING", "Pending"), ("APPROVED", "Approved"), ("REJECTED", "Rejected")))
    completed_at = models.DateTimeField(blank=True, null=True)

    # Added brand field with default value
    brand = models.CharField(max_length=200, default="mess for")

    class Meta:
        ordering = ("user",)
        verbose_name = _("Preference")
        verbose_name_plural = _("Preferences")

    def get_addresses(self):
        return DeliveryAddress.objects.filter(preferance=self)

    def __str__(self):
        return f"{self.session_id}"


class DeliveryAddress(BaseModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="delivery_addresses", blank=True, null=True)
    preferance = models.ForeignKey(Preference, on_delete=models.CASCADE, related_name="delivery_addresses")
    room_no = models.CharField(max_length=200)
    floor = models.CharField(max_length=200)
    building_name = models.CharField(max_length=200)
    street_name = models.CharField(max_length=200)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="delivery_area")
    contact_number = models.CharField(max_length=200)
    address_type = models.CharField(max_length=200, choices=(("Home","Home"),("Office", "Office")))
    location = models.URLField("Location Map Link", max_length=200, blank=True, null=True)
    is_default = models.BooleanField("Set as default delivery address", default=False)

    class Meta:
        ordering = ("user",)
        verbose_name = _("Delivery Address")
        verbose_name_plural = _("Delivery Addresses")

    def __str__(self):
        return f"{self.address_type.upper()} : {self.room_no}, {self.floor}, {self.building_name}, {self.street_name}, {self.area}"


class Subscription(BaseModel):
    request = models.ForeignKey("main.SubscriptionRequest", on_delete=models.CASCADE, related_name="subscription_requests")
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="subscription_plan")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ("start_date",)
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    def get_absolute_url(self):
        return reverse_lazy("main:subscription_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("main:subscription_list")

    def save(self, *args, **kwargs):
        self.end_date = self.start_date + timezone.timedelta(days=self.plan.validity)
        # create_orders(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.plan} - {self.start_date}"


class MealOrder(BaseModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="usermeals")
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name="itemmeals")
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="mealsplan")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="meals")
    date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=200, default="PENDING", choices=ORDER_STATUS_CHOICES)
    is_donated = models.BooleanField(default=False)

    def flag(self):
        data = {
            "PENDING": "warning",
            "IN_PREPERATION": "info",
            "IN_TRANSIT": "primary",
            "DELIVERED": "success",
            "CANCELLED": "danger",
        }
        return data[self.status]

    def get_absolute_url(self):
        return reverse("main:history_detail_view", kwargs={"pk": self.pk})

    def get_address(self):
        req = self.subscription.request
        if self.item.mealtype == "BREAKFAST":
            return f"Room: {req.breakfast_address_room_no}, {req.breakfast_address_floor}, {req.breakfast_address_building_name}, {req.breakfast_address_street_name}, {req.breakfast_address_area}"
        if self.item.mealtype == "LUNCH":
            return f"Room: {req.lunch_address_room_no}, {req.lunch_address_floor}, {req.lunch_address_building_name}, {req.lunch_address_street_name}, {req.lunch_address_area}"
        if self.item.mealtype == "DINNER":
            return f"Room: {req.dinner_address_room_no}, {req.dinner_address_floor}, {req.dinner_address_building_name}, {req.dinner_address_street_name}, {req.dinner_address_area}"
        if self.item.mealtype == "TIFFIN_LUNCH":
            return f"Room: {req.lunch_address_room_no}, {req.lunch_address_floor}, {req.lunch_address_building_name}, {req.lunch_address_street_name}, {req.lunch_address_area}"

    def mealtype(self):
        """Return meal type for admin display"""
        return self.item.mealtype if self.item else ""

    def DocNum(self):
        """Return empty string as shown in Excel"""
        return ""

    def Series(self):
        """Return dynamic series based on area or branch"""
        try:
            req = self.subscription.request
            
            # Based on area
            if req.breakfast_address_area:
                area_code = req.breakfast_address_area.pk
                return 70 + (area_code % 10)
            elif req.lunch_address_area:
                area_code = req.lunch_address_area.pk
                return 70 + (area_code % 10)
            elif req.dinner_address_area:
                area_code = req.dinner_address_area.pk
                return 70 + (area_code % 10)
            elif self.item.meal_category:
                category_code = self.item.meal_category.pk
                return 70 + (category_code % 10)
                
            return 70
        except:
            return 70

    def DocDate(self):
        """Return date in YYYYMMDD format as integer"""
        return int(self.date.strftime("%Y%m%d"))

    def DocDueDate(self):
        """Return same as DocDate"""
        return int(self.date.strftime("%Y%m%d"))

   
    def CardCode(self):
        """Return mobile number from meal preference"""
        try:
            # Check if we have the full relationship chain
            if (self.subscription and 
                self.subscription.request and 
                self.subscription.request.user):
                
                user = self.subscription.request.user
                
                # Get the user's preferences and find one with mobile
                preferences = user.preferences.all()
                
                for preference in preferences:
                    if preference.mobile:
                        return preference.mobile
                
                # If no mobile found in any preference, return empty string
                return ""
            
            return ""
        except Exception as e:
            # For debugging - you can remove this print later
            print(f"CardCode error for MealOrder {self.id}: {e}")
            return ""

    def U_OrderType(self):
        """Return Veg/Non Veg based on item database field"""
        return "Veg" if self.item.is_veg else "Non Veg"

    def U_Order_Catg(self):
        """Return order category based on meal category from database"""
        try:
            return self.item.meal_category.name if self.item.meal_category else "General"
        except:
            return "General"

    def U_MealType(self):
        """Return meal type in title case"""
        meal_type_mapping = {
            'BREAKFAST': 'Breakfast',
            'EARLY_BREAKFAST': 'Breakfast',
            'LUNCH': 'Lunch',
            'TIFFIN_LUNCH': 'Lunch',
            'DINNER': 'Dinner'
        }
        return meal_type_mapping.get(self.item.mealtype, self.item.mealtype.title())

    def U_Zone(self):
        """Return the area/zone name based on meal type's delivery address"""
        try:
            req = self.subscription.request
            
            if self.item.mealtype in ["BREAKFAST", "EARLY_BREAKFAST"]:
                return req.breakfast_address_area.name if req.breakfast_address_area else ""
            elif self.item.mealtype in ["LUNCH", "TIFFIN_LUNCH"]:
                return req.lunch_address_area.name if req.lunch_address_area else ""
            elif self.item.mealtype == "DINNER":
                return req.dinner_address_area.name if req.dinner_address_area else ""
            else:
                # Fallback to the general area field
                return req.area.name if req.area else ""
        except:
            return ""

    def U_Driver(self):
        """Return the full name of the delivery staff from the subscription request"""
        try:
            subscription_request = self.subscription.request
            if subscription_request.delivery_staff:
                # Try to get the full name, fallback to username
                staff = subscription_request.delivery_staff
                if hasattr(staff, 'first_name') and hasattr(staff, 'last_name'):
                    full_name = f"{staff.first_name} {staff.last_name}".strip()
                    if full_name:
                        return full_name
                # Fallback to username
                return staff.username
            else:
                return ""
        except (AttributeError, Exception):
            return ""

    def U_DT(self):
        """Return delivery time based on meal type and subscription request"""
        try:
            req = self.subscription.request
            
            if self.item.mealtype in ["BREAKFAST", "EARLY_BREAKFAST"]:
                time_display = req.get_breakfast_time_display() if hasattr(req, 'get_breakfast_time_display') else ""
            elif self.item.mealtype in ["LUNCH", "TIFFIN_LUNCH"]:
                time_display = req.get_lunch_time_display() if hasattr(req, 'get_lunch_time_display') else ""
            elif self.item.mealtype == "DINNER":
                time_display = req.get_dinner_time_display() if hasattr(req, 'get_dinner_time_display') else ""
            else:
                return ""
                
            # Extract the start time (before "to")
            if time_display and "to" in time_display:
                return time_display.split("to")[0].strip()
            else:
                return time_display or ""
        except:
            return ""

    def Comments(self):
        """Return comments from subscription request or notes"""
        try:
            comments = []
            
            if self.subscription.request.notes:
                comments.append(self.subscription.request.notes)
            
            if self.subscription.request.remarks:
                comments.append(self.subscription.request.remarks)
                
            return "; ".join(comments) if comments else ""
        except:
            return ""

    def U_DAddress(self):
        """Return complete delivery address based on meal type"""
        try:
            req = self.subscription.request
            
            if self.item.mealtype in ["BREAKFAST", "EARLY_BREAKFAST"]:
                address_parts = [
                    req.breakfast_address_room_no,
                    req.breakfast_address_floor,
                    req.breakfast_address_building_name,
                    req.breakfast_address_street_name,
                    req.breakfast_address_area.name if req.breakfast_address_area else None
                ]
            elif self.item.mealtype in ["LUNCH", "TIFFIN_LUNCH"]:
                address_parts = [
                    req.lunch_address_room_no,
                    req.lunch_address_floor,
                    req.lunch_address_building_name,
                    req.lunch_address_street_name,
                    req.lunch_address_area.name if req.lunch_address_area else None
                ]
            elif self.item.mealtype == "DINNER":
                address_parts = [
                    req.dinner_address_room_no,
                    req.dinner_address_floor,
                    req.dinner_address_building_name,
                    req.dinner_address_street_name,
                    req.dinner_address_area.name if req.dinner_address_area else None
                ]
            else:
                return ""
            
            # Filter out None/empty values and join
            filtered_parts = [str(part) for part in address_parts if part]
            return ", ".join(filtered_parts) if filtered_parts else ""
            
        except Exception as e:
            return ""

    def ParentKey(self):
        """Return DocNum (empty string) as parent key"""
        return ""

    def LineNum(self):
        """Return line number - always 1 as shown in Excel"""
        return 1

    def Quantity(self):
        """Return quantity"""
        return self.quantity

    def ItemCode(self):
        """Return item code"""
        return self.item.item_code

    def PriceAfterVAT(self):
        """Return meal fee from subscription request"""
        try:
            return float(self.subscription.request.meal_fee)
        except:
            return float(self.item.price)

    def PriceAfVAT(self):
        """Return meal fee from subscription request (for second header row - Excel format)"""
        try:
            return float(self.subscription.request.meal_fee)
        except:
            return float(self.item.price)

    def CostingCode(self):
        """Return costing code (for first header row)"""
        try:
            if self.item.category:
                return self.item.category.name
            elif self.item.meal_category:
                return self.item.meal_category.name
            else:
                return "Mess For"
        except:
            return "Mess For"

    def OcrCode(self):
        """Return brand from user's preference, defaulting to 'mess for'"""
        try:
            # Try to get brand from user's preferences first
            preference = self.user.preferences.first()
            if preference and preference.brand:
                return preference.brand
            else:
                return "mess for"
        except:
            return "mess for"

    def map(self):
        """Return map location based on meal type"""
        try:
            req = self.subscription.request
            if self.item.mealtype in ["BREAKFAST", "EARLY_BREAKFAST"]:
                return req.breakfast_location
            elif self.item.mealtype in ["LUNCH", "TIFFIN_LUNCH"]:
                return req.lunch_location
            elif self.item.mealtype == "DINNER":
                return req.dinner_location
            return None
        except:
            return None

    def delivery_time(self):
        """Alias for U_DT"""
        return self.U_DT()

    def __str__(self):
        return f"{self.item} - {self.date}"

    class Meta:
        ordering = ("date",)
        verbose_name = _("Meal Order")
        verbose_name_plural = _("Meal Orders")


class SubscriptionRequest(BaseModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="subscription_requests")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="subscription_requests", blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    breakfast_address_room_no = models.CharField(max_length=200, blank=True, null=True)
    breakfast_address_floor = models.CharField(max_length=200, blank=True, null=True)
    breakfast_address_building_name = models.CharField(max_length=200, blank=True, null=True)
    breakfast_address_street_name = models.CharField(max_length=200, blank=True, null=True)
    breakfast_address_area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="breakfast_address_area", blank=True, null=True)
    breakfast_time = models.CharField("Delivery Time (Breakfast)", max_length=200, choices=BREAKFAST_DELIVERY_CHOICES, default="0900:0930")
    breakfast_location = models.URLField("Location Map Link", max_length=200, blank=True, null=True)

    lunch_address_room_no = models.CharField(max_length=200, blank=True, null=True)
    lunch_address_floor = models.CharField(max_length=200, blank=True, null=True)
    lunch_address_building_name = models.CharField(max_length=200, blank=True, null=True)
    lunch_address_street_name = models.CharField(max_length=200, blank=True, null=True)
    lunch_address_area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="lunch_address_area", blank=True, null=True)
    lunch_time = models.CharField("Delivery Time (Lunch", max_length=200, choices=LUNCH_DELIVERY_CHOICES, default="1230:1300")
    lunch_location = models.URLField("Location Map Link", max_length=200, blank=True, null=True)

    dinner_address_room_no = models.CharField(max_length=200, blank=True, null=True)
    dinner_address_floor = models.CharField(max_length=200, blank=True, null=True)
    dinner_address_building_name = models.CharField(max_length=200, blank=True, null=True)
    dinner_address_street_name = models.CharField(max_length=200, blank=True, null=True)
    dinner_address_area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="dinner_address_area", blank=True, null=True)
    dinner_time = models.CharField("Delivery Time (Dinner)", max_length=200, choices=DINNER_DELIVERY_CHOICES, default="2100:2130")
    dinner_location = models.URLField("Location Map Link", max_length=200, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=200, default="PENDING", choices=(("PENDING", "Pending"), ("APPROVED", "Approved"), ("REJECTED", "Rejected")))
    remarks = models.TextField(blank=True, null=True)
    stage = models.CharField(
        max_length=200,
        default="OBJECT_CREATED",
        choices=(("OBJECT_CREATED", "OBJECT_CREATED"), ("PLAN_SELECTED", "PLAN_SELECTED"), ("ADDRESS_ADDED", "ADDRESS_ADDED"), ("COMPLETED", "COMPLETED")),
    )
    completed_at = models.DateTimeField(blank=True, null=True)

    approved_by = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="approved_requests", blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    area = models.ForeignKey("main.Area", verbose_name=_("Zone"), on_delete=models.CASCADE, blank=True, null=True)
    delivery_staff = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="driver_requests", blank=True, null=True, limit_choices_to={"usertype": "Delivery"})
    meal_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    no_of_meals = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("start_date",)
        verbose_name = _("Subscription Request")
        verbose_name_plural = _("Subscription Requests")

    def get_absolute_url(self):
        return reverse("main:subscriptionrequest_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse("main:subscriptionrequest_list")

    def get_update_url(self):
        return reverse("main:subscriptionrequest_update", kwargs={"pk": self.pk})

    def get_approve_url(self):
        return reverse("main:subscriptionrequest_approve", kwargs={"pk": self.pk})

    def get_reject_url(self):
        return reverse("main:subscriptionrequest_reject", kwargs={"pk": self.pk})

    def get_print_url(self):
        return reverse("main:subscriptionrequest_print", kwargs={"pk": self.pk})

    def mealtypes(self):
        if self.plan:
            return set(self.plan.available_mealtypes)

    def __str__(self):
        return f"{self.user} - {self.plan} - {self.start_date}"


def create_orders(subscription):
    for i in range(subscription.plan.validity):
        date = subscription.start_date + timezone.timedelta(days=i)
        items = ItemMaster.objects.filter(is_active=True, meal_category=subscription.plan.meal_category)
        for item in items:
            MealOrder.objects.get_or_create(user=subscription.user, item=item, subscription=subscription, subscription_plan=subscription.plan, date=date)
    return True