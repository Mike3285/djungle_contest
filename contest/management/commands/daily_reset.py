import os
import logging
from django.core.management.base import BaseCommand, CommandError
from contest.models import Prize
from datetime import datetime
from django.conf import settings

logging.basicConfig(filename=os.path.join(settings.BASE_DIR, "zeroing_log.log"),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.DEBUG)


class Command(BaseCommand):
    help = 'Sets the number of daily wins to 0 an all prizes when invoked and extracts winning moments of the day for every prize'

    def handle(self, *args, **options):
        try:
            prizes = Prize.objects.all()
            prizes.update(won_today=0)
            for i in prizes:
                i.make_winning_timestamps()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            logging.debug(f"Reset completed at {now}\n")
            print(f"Zeroing done at {now}\n")
        except Exception as e:
            logging.error(f"An error occured. Exception: {e}\n")
