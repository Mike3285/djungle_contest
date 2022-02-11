import datetime
import json
import random

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from .utils import random_date


# Create your models here.

class MyModel(models.Model):
    last_updated = models.DateTimeField(auto_now=True,
                                        editable=False,
                                        null=True,
                                        verbose_name=_('Last updated'),
                                        help_text=_("Date&time of the latest update"))
    created = models.DateTimeField(auto_now_add=True,
                                   editable=False,
                                   null=True,
                                   verbose_name=_('Created'),
                                   help_text=_("Date&time of creation"))

    class Meta:
        abstract = True


class Utente(AbstractUser):
    WMAX = models.IntegerField(verbose_name=_("Max wins perday"),
                               help_text=_("Number of times this user can win a single contest"),
                               default=1,
                               blank=True,
                               null=False)
    won_contests = models.JSONField(verbose_name=_("Won contests today"),
                                    help_text=_("Contests this user won today"),
                                    blank=True,
                                    null=True)


class Contest(MyModel):
    name = models.CharField(verbose_name=_("Name"),
                            max_length=255,
                            help_text=_("Contest's name or details"),
                            blank=False,
                            null=False, )

    start_date = models.DateField(verbose_name=_('Starting date'),
                                  help_text=_("Contest's starting date (included)"),
                                  blank=False,
                                  null=False, )
    stop_date = models.DateField(verbose_name=_('Ending date'),
                                 help_text=_("Contest's ending date (included)"),
                                 blank=False,
                                 null=False, )
    code = models.CharField(verbose_name=_("Code"),
                            unique=True,
                            max_length=5,
                            help_text=_("Contest's unique code"),
                            blank=False,
                            null=False,
                            db_index=True)

    allowed_users = models.ManyToManyField("contest.Utente",
                                           related_name="allowed_contests",
                                           verbose_name=_("Allowed users"),
                                           help_text=_("Users allowed to participate to this contest"))

    def __str__(self):
        return "Contest " + self.code

    class Meta:
        verbose_name = _('Contest')
        verbose_name_plural = _('Contests')


class Prize(MyModel):
    name = models.CharField(verbose_name=_("Name"),
                            max_length=255,
                            help_text=_("Prize's name or details"),
                            blank=False,
                            null=False, )

    code = models.CharField(verbose_name=_("Code"),
                            unique=True,
                            max_length=255,
                            help_text=_("Prize's unique code"),
                            blank=False,
                            null=False,
                            db_index=True)

    perday = models.IntegerField(verbose_name=_("Per day"),
                                 help_text=_("Prize's maximum wins in a single day"),
                                 blank=False,
                                 null=False)

    winning_timestamps = models.JSONField(verbose_name=_("Winning timestamps"),
                                          help_text=_("Today's winning timestamps"),
                                          blank=True,
                                          null=True)

    won_today = models.IntegerField(verbose_name=_("Won today"),
                                    help_text=_("Number of times the prize has been won today"),
                                    default=0,
                                    blank=True,
                                    null=False)

    contest_field = models.OneToOneField("contest.Contest",
                                         on_delete=models.CASCADE,
                                         verbose_name=_("Contest"),
                                         help_text=_("Contest with this prize"),
                                         related_name="prize_field")

    def make_winning_timestamps(self):
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        winning_intervals = [today + i * (datetime.timedelta(days=1) // self.perday)
                             for i in range(self.perday)]

        winning_moments = {
            random_date(winning_intervals[i], winning_intervals[i + 1]) if i != len(
                winning_intervals) - 1
            else random_date(winning_intervals[i], datetime.datetime.now().replace(hour=23, minute=59, second=59,
                                                                                   microsecond=999999)): False
            for i in range(len(winning_intervals))
        }
        self.winning_timestamps = json.dumps(winning_moments, )
        if not self._state.adding is True:
            self.save()

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            self.make_winning_timestamps()
        super(Prize, self).save(*args, **kwargs)

    def __str__(self):
        return "Prize " + self.code

    class Meta:
        verbose_name = _('Prize')
        verbose_name_plural = _('Prizes')
