from django import template

register = template.Library()

@register.filter
def filter_by_type(queryset, type_name):
    """Фильтрует QuerySet категорий по типу"""
    return queryset.filter(type=type_name)

@register.filter
def income_categories(queryset):
    """Возвращает только категории доходов"""
    return queryset.filter(type='income')

@register.filter
def expense_categories(queryset):
    """Возвращает только категории расходов"""
    return queryset.filter(type='expense')