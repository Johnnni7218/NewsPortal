from datetime import timedelta, datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from news.models import Category, Post


@shared_task
def send_weekly_article_list():
    start_date = datetime.today() - timedelta(days=6)
    this_weeks_posts = Post.objects.filter(time_post__gt=start_date)
    for cat in Category.objects.all():
        post_list = this_weeks_posts.filter(category=cat)
        if post_list:
            subscribers = cat.subscribers.values('username', 'email')
            recipients = []
            for sub in subscribers:
                recipients.append(sub['email'])

            msg = EmailMultiAlternatives(
                subject=f'{cat.name}: Посты за прошедшую неделю',
                body=" ",
                from_email='settings.DEFAULT_FROM_EMAIL',
                to=recipients
            )