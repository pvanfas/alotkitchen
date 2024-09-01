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

MEALTYPE_CHOICES = (("BREAKFAST", "Break Fast"), ("LUNCH", "Lunch"), ("TIFFIN_LUNCH", "Tiffin Lunch"), ("DINNER", "Dinner"))
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

BREAKFAST_DELIVERY_CHOICES = (
    ("0630:0700", "6:30 am to 7 am"),
    ("0700:0730", "7 am to 7:30 am"),
    ("0730:0800", "7:30 am to 8 am"),
    ("0800:0830", "8 am to 8:30 am"),
    ("0900:0930", "9 am to 9:30 am"),
)

LUNCH_DELIVERY_CHOICES = (
    ("1230:1300", "12:30 pm to 1 pm"),
    ("1300:1330", "1 pm to 1:30 pm"),
    ("1330:1400", "1:30 pm to 2 pm"),
    ("1400:1430", "2 pm to 2:30 pm"),
    ("1430:1500", "2:30 pm to 3 pm"),
)

DINNER_DELIVERY_CHOICES = (
    ("1930:2000", "7:30 pm to 8 pm"),
    ("2000:2030", "8 pm to 8:30 pm"),
    ("2030:2100", "8:30 pm to 9 pm"),
    ("2100:2130", "9 pm to 9:30 pm"),
    ("2130:2200", "9:30 pm to 10 pm"),
)
