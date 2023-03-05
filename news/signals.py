from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post


@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        subscribers = instance.categories.values(
            'subscribers__email', 'subscribers__username'
        )
        for subscriber in subscribers:
            html_content = render_to_string(
                'post_email.html',
                {
                    'post': instance,
                    'username': subscriber.get("subscribers__username")
                }
            )

            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=instance.text,
                from_email='ilya.mikhassik@yandex.ru',
                to=[subscriber.get("subscribers__email")]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
