import calendar
import datetime

import pytz
from django.utils.text import slugify

BOOL_CHOICES = ((True, "Yes"), (False, "No"))
GENDER_CHOICES = (("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other"))
RATING_CHOICES = ((1, "One"), (2, "Two"), (3, "Three"), (4, "Four"), (5, "Five"))
SALUTATION_CHOICES = (("Dr.", "Dr."), ("Miss", "Miss"), ("Mr", "Mr"), ("Mrs", "Mrs"), ("Prof.", "Prof."))
YEAR_CHOICES = [(y, y) for y in range(1950, datetime.date.today().year + 2)]
MONTH_CHOICES = [(i, calendar.month_name[i]) for i in range(1, 13)]
TIMEZONES = [(tz, tz) for tz in pytz.common_timezones]
SELECTION_CHOICES = (("", "Select"), ("yes", "Yes"), ("no", "No"))


INDUSTRY_CHOICES_LIST = [
    "Agency or Sales House",
    "Agriculture",
    "Art and Design",
    "Automotive",
    "Construction",
    "Consulting",
    "Consumer Packaged Goods",
    "Education",
    "Engineering",
    "Entertainment",
    "Financial Services",
    "Food Services (Restaurants/Fast Food)",
    "Gaming",
    "Government",
    "Health Care",
    "Interior Design",
    "Internal",
    "Legal",
    "Manufacturing",
    "Marketing",
    "Mining and Logistics",
    "Non-Profit",
    "Publishing and Web Media",
    "Real Estate",
    "Retail (E-Commerce and Offline)",
    "Services",
    "Technology",
    "Telecommunications",
    "Travel/Hospitality",
    "Web Designing",
    "Web Development",
    "Writer",
    "Other",
]
INDUSTRY_CHOICES = [(slugify(industry), industry) for industry in INDUSTRY_CHOICES_LIST]
STAFF_STATUS = (("active", "Active"), ("resigned", "Resigned"), ("terminated", "Terminated"))
PROJECT_CHOICES = (("website", "Website"), ("webApp", "Web App"), ("Ecommerce", "Ecommerce"), ("ERP", "ERP"))
STACK_CHOICES = (
    ("Django", "Django"),
    ("Static HTML", "Static HTML"),
    ("LAMP", "LAMP"),
    ("MEAN", "MEAN"),
    ("MERN", "MERN"),
    ("Flask", "Flask"),
    ("React", "React"),
    ("Angular", "Angular"),
    ("Vue", "Vue"),
    ("Wordpress", "Wordpress"),
    ("Shopify", "Shopify"),
    ("Magento", "Magento"),
    ("Prestashop", "Prestashop"),
    ("WooCommerce", "WooCommerce"),
)
DOMAIN_OWNER_CHOICES = (
    ("Client", "Client"),
    ("Company Namecheap", "Company Namecheap"),
    ("Company Godaddy", "Company Godaddy"),
    ("Company AEServer", "Company AEServer"),
)
DNS_MANAGER_CHOICES = (
    ("Namecheap DNS", "Namecheap DNS"),
    ("Godaddy DNS", "Godaddy DNS"),
    ("DigitalOcean DNS", "DigitalOcean DNS"),
    ("AWS Route 53", "AWS Route 53"),
    ("Azure DNS", "Azure DNS"),
    ("Cloudflare DNS", "Cloudflare DNS"),
    ("Custom DNS", "Custom DNS"),
)
PAYMENT_METHOD_CHOICES = (("CASH", "Cash"), ("CHEQUE", "Cheque"), ("BANK", "Bank Transfer"), ("CARD", "Card Payment"))
