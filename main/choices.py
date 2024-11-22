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
    ("0630:0700", "6:30AM to 7AM"),
    ("0700:0730", "7AM to 7:30AM"),
    ("0730:0800", "7:30AM to 8AM"),
    ("0800:0830", "8AM to 8:30AM"),
    ("0900:0930", "9AM to 9:30AM"),
)

LUNCH_DELIVERY_CHOICES = (
    ("1230:1300", "12:30PM to 1PM"),
    ("1300:1330", "1PM to 1:30PM"),
    ("1330:1400", "1:30PM to 2PM"),
    ("1400:1430", "2PM to 2:30PM"),
    ("1430:1500", "2:30PM to 3PM"),
)

DINNER_DELIVERY_CHOICES = (
    ("1930:2000", "7:30PM to 8PM"),
    ("2000:2030", "8PM to 8:30PM"),
    ("2030:2100", "8:30PM to 9PM"),
    ("2100:2130", "9PM to 9:30PM"),
    ("2130:2200", "9:30PM to 10PM"),
)
GROUP_CHOICES = (
    ("ESSENTIAL", "Essential"),
    ("REGULAR", "Regular"),
    ("DELUXE", "Deluxe"),
    ("STANDARD", "Standard"),
)
