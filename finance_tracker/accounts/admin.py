from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
