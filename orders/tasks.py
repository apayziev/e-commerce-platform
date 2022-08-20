from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from core.local_settings import personal_email


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f"Order nr. {order.id}"
    message = f"Dear {order.first_name},\n\nYou have successfully placed an order. Your order id is {order.id}."

    mail_sent = send_mail(
        subject,
        message,
        personal_email,
        [order.email],
    )

    return mail_sent
