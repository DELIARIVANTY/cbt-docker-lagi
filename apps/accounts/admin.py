from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'kelas', 'plain_password', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'kelas', 'ampu_mapel', 'plain_password')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'kelas', 'ampu_mapel', 'plain_password')}),
    )
    filter_horizontal = ('ampu_mapel',)

admin.site.register(CustomUser, CustomUserAdmin)
