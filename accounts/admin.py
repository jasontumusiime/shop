from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account


class AccountAdmin(UserAdmin):
    list_display = (
        'email', 
        'first_name', 
        'last_name', 
        'username', 
        'last_login',
        'date_joined',
        'is_active',
    )
    # list_display_links = ('email', 'first_name', 'last_name', 'username',)
    list_display_links = ('is_active',)
    readonly_fields = ('last_login', 'date_joined')
    # ordering = ('-date_joined',)
    # Silence unreferred field errors
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)