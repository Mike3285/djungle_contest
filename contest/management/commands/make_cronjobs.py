import os

from django.core.management.base import BaseCommand, CommandError
from contest.models import Prize
from crontab import CronTab
from django.conf import settings


class Command(BaseCommand):
    help = 'Adds the required cronjob to reset contests at midnight'

    def handle(self, *args, **options):
        print(f'python3 {os.path.join(settings.BASE_DIR, "manage.py daily_zeroing")}')
        cron = CronTab(user="root")
        job = cron.new(command=f'python3 {os.path.join(settings.BASE_DIR, "manage.py daily_zeroing")}')
        job.day.every(1)
        cron.write()



