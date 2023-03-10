from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.utils.timezone import datetime

from datetime import timedelta

from .models import Post, Category


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


@shared_task
def send_weekly_email():
    start_date = datetime.today() - timedelta(days=6)
    this_weeks_posts = Post.objects.filter(created_on__gt=start_date)
    for cat in Category.objects.all():
        post_list = this_weeks_posts.filter(categories=cat)
        if post_list:
            subscribers = cat.subscribers.values('username', 'email')
            recipients = []
            for sub in subscribers:
                recipients.append(sub['email'])

            html_content = render_to_string(
                'weekly_post_email.html', {
                    'post_list': post_list.values('pk', 'title').order_by('-created_on'),
                    'domain': Site.objects.get_current().domain,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'{cat.name}: Посты за прошедшую неделю',
                body="post_list",
                from_email='ilya.mikhassik@yandex.ru',
                to=recipients
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
