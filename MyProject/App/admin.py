from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AdminSiteUsers, AppUsers, Tasks


@admin.register(AdminSiteUsers)
class AdminUserAdmin(UserAdmin):
    pass
    # readonly_fields = ['id']
    # アドミンサイトのカスタマイズは今回は最低限にとどめました

@admin.register(AppUsers)
class AppUsersAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at']

@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created_at', 'update_at']