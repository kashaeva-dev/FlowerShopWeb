from django.contrib import admin

from .models import Staff


@admin.register(Staff)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'start_date', 'end_date', 'tg_id']
