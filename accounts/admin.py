from django.contrib import admin
from .models import User
from django.utils.dateformat import format as date_format


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("email",)
    list_display = ("id", "email", "created_formatted")
    list_filter = ("created",)

    def created_formatted(self, obj):
        return date_format(obj.created, 'Y-m-d H:i:s')
