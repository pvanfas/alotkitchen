import calendar
import datetime

import pytz

BOOL_CHOICES = ((True, "Yes"), (False, "No"))
GENDER_CHOICES = (("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other"))
RATING_CHOICES = ((1, "One"), (2, "Two"), (3, "Three"), (4, "Four"), (5, "Five"))
SALUTATION_CHOICES = (("Dr.", "Dr."), ("Miss", "Miss"), ("Mr", "Mr"), ("Mrs", "Mrs"), ("Prof.", "Prof."))
YEAR_CHOICES = [(y, y) for y in range(1950, datetime.date.today().year + 2)]
MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]
TIMEZONES = [(tz, tz) for tz in pytz.common_timezones]
SELECTION_CHOICES = (("", "Select"), ("yes", "Yes"), ("no", "No"))
STAFF_STATUS = (("active", "Active"), ("resigned", "Resigned"), ("terminated", "Terminated"))
PROJECT_CHOICES = (("website", "Website"), ("webApp", "Web App"), ("Ecommerce", "Ecommerce"), ("ERP", "ERP"))
PAYMENT_METHOD_CHOICES = (("CASH", "Cash"), ("CHEQUE", "Cheque"), ("BANK", "Bank Transfer"), ("CARD", "Card Payment"))
