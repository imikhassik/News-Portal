from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    # subscribers = instance.categories.values(
    #     'subscribers__email', 'subscribers__username'
    # )
    # for subscriber in subscribers:
    #     html_content = render_to_string(
    #         'post_email.html',
    #         {
    #             'post': instance,
    #             'username': subscriber.get("subscribers__username")
    #         }
    #     )
    #
    #     msg = EmailMultiAlternatives(
    #         subject=instance.title,
    #         body=instance.text,
    #         from_email='ilya.mikhassik@yandex.ru',
    #         to=[subscriber.get("subscribers__email")]
    #     )
    #     msg.attach_alternative(html_content, "text/html")
    #     msg.send()
    print(instance.categories.all())
