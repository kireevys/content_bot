from django.contrib import admin

# Register your models here.
import main.models.common


@admin.register(main.models.common.User)
class UserAdmin(admin.ModelAdmin):
    """Админка для юзеров."""

    ordering = ("id",)
    date_hierarchy = "add_date"


@admin.register(main.models.common.Static)
class StaticAdmin(admin.ModelAdmin):
    """Админка статики."""

    ordering = ("slug",)
