from django.db import models
from django.conf import settings


class Category(models.Model):
    CATEGORY_TYPES = (
        ('expense', 'Расход'),
        ('income', 'Доход'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории'
    )
    type = models.CharField(
        max_length=10,
        choices=CATEGORY_TYPES,
        verbose_name='Тип категории'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создана'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлена'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['type', 'name']
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"