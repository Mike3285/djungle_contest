import os
import getpass

from django.core.management.base import BaseCommand, CommandError
from contest.models import Prize
from crontab import CronTab
from django.conf import settings


class Command(BaseCommand):
    help = 'Adds the required cronjob to reset contests at midnight'

    def handle(self, *args, **options):
        print("Making the cronjob...")
        cron = CronTab(user=settings.CRON_USER)
        empty_cron = CronTab()
        temp_job = empty_cron.new(
            command=f'{os.path.join(settings.BASE_DIR, "venv/bin/python3")} {os.path.join(settings.BASE_DIR, "manage.py")} daily_reset >> {os.path.join(settings.BASE_DIR, "make_cronjobs.log")} 2>&1 | logger &'
        )
        temp_job.every(1).days()
        if not temp_job in cron.crons:
            job = cron.new(
                command=f'{os.path.join(settings.BASE_DIR, "venv/bin/python3")} {os.path.join(settings.BASE_DIR, "manage.py")} daily_reset >> {os.path.join(settings.BASE_DIR, "make_cronjobs.log")} 2>&1 | logger &'
            )
            # DEBUG
            job.every(1).days()
            cron.write()
        else:
            print("The same cronjob was already present")

        print("Done! You can check with \"crontab -e\" that everything went correctly")
