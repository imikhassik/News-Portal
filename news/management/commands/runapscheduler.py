import logging

from django.conf import settings
from django.utils.timezone import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from datetime import timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post, Category

logger = logging.getLogger(__name__)


def my_job():
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

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
