# Generated by Django 4.0.1 on 2022-01-30 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='Date&time of the latest update', null=True, verbose_name='Last updated')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date&time of creation', null=True, verbose_name='Created')),
                ('name', models.CharField(help_text="Contest's name or details", max_length=255, verbose_name='Name')),
                ('start_date', models.DateField(help_text="Contest's starting date (included)", verbose_name='Starting date')),
                ('stop_date', models.DateField(help_text="Contest's ending date (included)", verbose_name='Ending date')),
                ('code', models.CharField(db_index=True, help_text="Contest's unique code", max_length=5, unique=True, verbose_name='Code')),
            ],
            options={
                'verbose_name': 'Contest',
                'verbose_name_plural': 'Contests',
            },
        ),
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True, help_text='Date&time of the latest update', null=True, verbose_name='Last updated')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date&time of creation', null=True, verbose_name='Created')),
                ('name', models.CharField(help_text="Prize's name or details", max_length=255, verbose_name='Name')),
                ('code', models.CharField(db_index=True, help_text="Prize's unique code", max_length=255, unique=True, verbose_name='Code')),
                ('perday', models.IntegerField(help_text="Prize's maxiumum wins in a single day", verbose_name='Per day')),
                ('won_today', models.IntegerField(default=0, help_text='Number of times the prize has been won today', verbose_name='Won today')),
                ('contest_field', models.OneToOneField(help_text='Contest with this prize', on_delete=django.db.models.deletion.CASCADE, related_name='prize_field', to='contest.contest', verbose_name='Contest')),
            ],
            options={
                'verbose_name': 'Prize',
                'verbose_name_plural': 'Prizes',
            },
        ),
    ]
