from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

USERTYPE_CHOICES = (
    ("Administrator", "Administrator"),
    ("BranchConvenor", "Branch Convenor"),
    ("User", "User"),
)


class CustomUser(AbstractUser):
    usertype = models.CharField(max_length=20, choices=USERTYPE_CHOICES, default="User")

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

    def __str__(self):
        return self.username
