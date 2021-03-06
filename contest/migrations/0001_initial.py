# Generated by Django 4.0.2 on 2022-02-04 23:15

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
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
                ('perday', models.IntegerField(help_text="Prize's maximum wins in a single day", verbose_name='Per day')),
                ('winning_timestamps', models.JSONField(blank=True, help_text="Today's winning timestamps", null=True, verbose_name='Winning timestamps')),
                ('won_today', models.IntegerField(blank=True, default=0, help_text='Number of times the prize has been won today', verbose_name='Won today')),
                ('contest_field', models.OneToOneField(help_text='Contest with this prize', on_delete=django.db.models.deletion.CASCADE, related_name='prize_field', to='contest.contest', verbose_name='Contest')),
            ],
            options={
                'verbose_name': 'Prize',
                'verbose_name_plural': 'Prizes',
            },
        ),
        migrations.CreateModel(
            name='Utente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('WMAX', models.IntegerField(blank=True, default=1, help_text='Number of times the prize can be', verbose_name='Max winning')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
