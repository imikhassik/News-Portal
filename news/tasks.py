from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from .models import Post


@shared_task
def notify_subscribers(pk):
    post = Post.objects.get(pk=pk)
    subscribers = post.categories.values(
        'subscribers__email', 'subscribers__username'
    )
    for subscriber in subscribers:
        html_content = render_to_string(
            'post_email.html',
            {
                'post': post,
                'username': subscriber.get("subscribers__username"),
                'domain': Site.objects.get_current().domain,
                'post_url': post.get_absolute_url(),
            }
        )

        msg = EmailMultiAlternatives(
            subject=post.title,
            body=post.text,
            from_email='ilya.mikhassik@yandex.ru',
            to=[subscriber.get("subscribers__email")],
            )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
