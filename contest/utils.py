import datetime
import random


def random_date(start, end):
    """Generate a random datetime between `start` and `end`"""
    date = start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
        microseconds=random.randint(0, 999999)
    )
    return date.strftime("%Y-%m-%d %H:%M:%S.%f")


