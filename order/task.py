# from celery import shared_task
from django.core.mail import send_mail
from order.models import Order
from django.conf import settings
from celery import shared_task


@shared_task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        # Handle the case where order doesn't exist
        return False
    email_from = settings.EMAIL_HOST
    subject = f'Order Number. {order.id}'
    message = f'Dear {order.get_username()},\n\n' \
              f'You have successfully placed an order.' \
              f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
                          message,
                          email_from,
                          [order.customer.email])
    return mail_sent
