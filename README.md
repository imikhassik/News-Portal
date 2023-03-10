# News-Portal (wip)
This project uses Django framework to create a web-portal where users can read and submit news and articles, comment 
and rate them. 
A user can subscribe to a category and receive emails when posts are added to this category. They also receive a 
weekly email with all the new posts in the category they subscribed to.

Signup, authentication and authorization implemented with django-allauth library.

Subscriber emailing and scheduling implemented with celery tasks.
Also, django signals and apscheduler jobs set up and commented out as an alternative.

This is a work in progress.
