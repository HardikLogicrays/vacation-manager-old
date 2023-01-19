
from django.shortcuts import render
from django.contrib import admin
from .models import User, Holiday


@admin.register(User)
class AdminUser(admin.ModelAdmin):

    list_display = ["emp_name", "email"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["password"]
        else:
            return []


@admin.register(Holiday)
class AdminHoliday(admin.ModelAdmin):

    list_display = ["email", "start_date", "end_date"]
    readonly_fields = ["event_id"]
