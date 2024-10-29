from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_admin_neworder_mail(instance):
    subject = "ALOT KITCHEN: New Subscription Request"
    message = f"New Subscription Request from {instance.user}"
    template = "email/admin_neworder.html"
    html_message = render_to_string(template, {"instance": instance})
    recipient_list = ["anfaspv.info@gmail.com"]
    send_mail(subject, message, settings.EMAIL_SENDER, recipient_list, html_message=html_message)


def send_customer_accepted_mail(instance):
    subject = "ALOT KITCHEN: Subscription Request Accepted"
    message = "Your Subscription Request has been accepted"
    template = "email/customer_accepted.html"
    html_message = render_to_string(template, {"instance": instance})
    recipient_list = [instance.user.email]
    send_mail(subject, message, settings.EMAIL_SENDER, recipient_list, html_message=html_message)


def send_customer_neworder_mail(instance):
    subject = "ALOT KITCHEN: New Subscription Request"
    message = f"New Subscription Request from {instance.user}"
    template = "email/customer_neworder.html"
    html_message = render_to_string(template, {"instance": instance})
    recipient_list = [instance.user.email]
    send_mail(subject, message, settings.EMAIL_SENDER, recipient_list, html_message=html_message)
