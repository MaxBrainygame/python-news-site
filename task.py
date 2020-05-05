from celery import Celery
from celery.schedules import crontab
from webapp import create_app
from webapp.news.parsers.habr import get_habr_snippets

flask_app = create_app()
celery_app = Celery('task', broker='redis://localhost:6379/0')


@celery_app.task
def habr_snippets():
    with flask_app.app_context():
        get_habr_snippets()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), habr_snippets.s())
