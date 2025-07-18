from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone

USERTYPE_CHOICES = (
    ("Administrator", "Administrator"),
    ("Manager", "Manager"),
    ("KitchenManager", "Kitchen Manager"),
    ("Delivery", "Delivery Staff"),
    ("Accountant", "Accountant Staff"),
    ("Customer", "Customer"),
)
LANGUAGE_CHOICES = (("en", "English"), ("ml", "Malayalam"), ("ar", "Arabic"), ("hi", "Hindi"), ("ta", "Tamil"), ("te", "Telugu"))


class CustomUser(AbstractUser):
    enc_key = models.UUIDField(default=uuid4, editable=False, unique=True)
    usertype = models.CharField(max_length=20, choices=USERTYPE_CHOICES, default="Customer")
    preferred_language = models.CharField("Language for verbal communication", max_length=10, choices=LANGUAGE_CHOICES, default="en")
    mobile = models.CharField(max_length=15, unique=True)
    alternate_mobile = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    @property
    def subscriptions(self):
        """
        A property to dynamically get all subscriptions for a user by querying
        through the Preference model's 'request' field.
        """
        from main.models import Subscription

        return Subscription.objects.filter(request__user=self)

    def active_subscriptions(self):
        """This method now works because self.subscriptions is available."""
        return self.subscriptions.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now(), is_active=True)

    def has_expired_subscription(self):
        """This method now works."""
        return self.subscriptions.filter(end_date__lt=timezone.now(), is_active=True).exists()

    @property
    def has_active_subscription(self):
        """This is better as a property and now works."""
        return self.active_subscriptions().exists()

    @property
    def subscription_ends_on(self):
        """
        This is safer and now works. It gets the end date of the latest
        active subscription, or None if there isn't one.
        """
        active_sub = self.active_subscriptions().order_by("-end_date").first()
        return active_sub.end_date if active_sub else None

    def has_zero_subscription(self):
        """This method now works."""
        return not self.subscriptions.filter(is_active=True).exists()

    def get_absolute_url(self):
        return reverse("main:customer_detail", args=[str(self.id)])

    def fullname(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        return self.username

    def __str__(self):
        return self.fullname()
