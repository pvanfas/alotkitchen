import calendar
import datetime

import pytz

BOOL_CHOICES = ((True, "Yes"), (False, "No"))
GENDER_CHOICES = (("MALE", "Male"), ("FEMALE", "Female"))
RATING_CHOICES = ((1, "One"), (2, "Two"), (3, "Three"), (4, "Four"), (5, "Five"))
SALUTATION_CHOICES = (("Dr.", "Dr."), ("Miss", "Miss"), ("Mr", "Mr"), ("Mrs", "Mrs"), ("Prof.", "Prof."))
YEAR_CHOICES = [(y, y) for y in range(1950, datetime.date.today().year + 2)]
MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]
TIMEZONES = [(tz, tz) for tz in pytz.common_timezones]
SELECTION_CHOICES = (("", "Select"), ("yes", "Yes"), ("no", "No"))
PAYMENT_METHOD_CHOICES = (("CASH", "Cash"), ("CHEQUE", "Cheque"), ("BANK", "Bank Transfer"), ("CARD", "Card Payment"))

MEALTYPE_CHOICES = (("BREAKFAST", "Break Fast"), ("LUNCH", "Lunch"), ("TIFFIN_LUNCH", "Tiffin Lunch"), ("DINNER", "Dinner"), ("ADDON", "Addon"))
WEEK_CHOICES = ((1, "1st & 3rd Week"), (2, "2nd & 4th Week"))
DAY_CHOICES = (
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday"),
)
VALIDITY_CHOICES = ((22, "22 Days"), (26, "26 Days"), (30, "30 Days"))
ORDER_STATUS_CHOICES = (("PENDING", "Pending"), ("IN_PREPERATION", "In Preparation"), ("IN_TRANSIT", "In Transit"), ("DELIVERED", "Delivered"), ("CANCELLED", "Cancelled"))
TIER_CHOICES = (
    ("Essential", "Essential"),
    ("ClassicVeg", "Classic Veg"),
    ("ClassicNonVeg", "Classic Non-Veg"),
    ("StandardNonVeg", "Standard Non-Veg"),
    ("StandardVeg", "Standard Veg"),
    ("Premium", "Premium"),
    ("Signature", "Signature"),
)
