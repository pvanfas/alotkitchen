from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone

USERTYPE_CHOICES = (
    ("Administrator", "Administrator"),
    ("KitchenManager", "Kitchen Manager"),
    ("Delivery", "Delivery Staff"),
    ("Customer", "Customer"),
)
LANGUAGE_CHOICES = (("en", "English"), ("ml", "Malayalam"), ("ar", "Arabic"), ("hi", "Hindi"), ("ta", "Tamil"), ("te", "Telugu"))


class CustomUser(AbstractUser):
    enc_key = models.UUIDField(default=uuid4, editable=False, unique=True)
    usertype = models.CharField(max_length=20, choices=USERTYPE_CHOICES, default="User")
    preferred_language = models.CharField("Language for verbal communication", max_length=10, choices=LANGUAGE_CHOICES, default="en")
    mobile = models.CharField(max_length=15, blank=True, null=True)
    alternate_mobile = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def active_subscriptions(self):
        return self.subscriptions.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now(), is_active=True)

    def has_expired_subscription(self):
        return self.subscriptions.filter(end_date__lt=timezone.now(), is_active=True).exists()

    def has_active_subscription(self):
        return self.active_subscriptions().exists()

    def subscription_ends_on(self):
        return self.active_subscriptions().first().end_date

    def has_zero_subscription(self):
        return not self.subscriptions.filter(is_active=True).exists()

    def get_absolute_url(self):
        return reverse("main:customer_detail", args=[str(self.id)])

    def fullname(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        elif self.first_name:
            return self.first_name
        return self.username

    def __str__(self):
        return self.fullname()
