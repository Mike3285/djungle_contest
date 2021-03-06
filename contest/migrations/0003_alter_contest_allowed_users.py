# Generated by Django 4.0.2 on 2022-02-05 00:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_contest_allowed_users_alter_utente_wmax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='allowed_users',
            field=models.ManyToManyField(help_text='Users allowed to participate to this contest', related_name='allowed_contests', to=settings.AUTH_USER_MODEL, verbose_name='Allowed users'),
        ),
    ]
