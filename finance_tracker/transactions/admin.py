from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'category', 'amount', 'account', 'user', 'description')
    list_filter = ('date', 'category__type', 'category', 'account', 'user')
    search_fields = ('description', 'category__name', 'account__name')
    date_hierarchy = 'date'
    ordering = ('-date', '-id')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'amount', 'date', 'category', 'account')
        }),
        ('Дополнительно', {
            'fields': ('description', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
