from django.utils.timezone import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from datetime import timedelta

from news.models import Post, Category


def weekly_email_job():
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
                    'post_list': post_list.values('pk', 'title'),
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
