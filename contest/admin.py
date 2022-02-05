from django.contrib import admin
from . import models


@admin.register(models.Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ['pk','code',  'name', 'start_date', 'stop_date']
    list_filter = ['name', 'start_date', 'stop_date']



@admin.register(models.Prize)
class PrizeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'code', 'name', 'perday','won_today', 'contest_field']
    list_filter = ['code', 'name', 'perday', 'contest_field']



@admin.register(models.Utente)
class UtenteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'username', 'WMAX']
    list_filter = ['username', 'WMAX']

