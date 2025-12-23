from django.db import models
from django.conf import settings
from django.urls import reverse


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('expense', 'Расход'),
        ('income', 'Доход'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Сумма'
    )
    date = models.DateField(
        verbose_name='Дата',
        db_index=True
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.PROTECT,
        verbose_name='Категория'
    )
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.PROTECT,
        verbose_name='Счет'
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Описание'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-date', '-id']
        indexes = [
            models.Index(fields=['-date', 'user']),
            models.Index(fields=['category', 'user']),
        ]

    def __str__(self):
        return f"{self.date}: {self.amount} - {self.category}"

    def get_absolute_url(self):
        return reverse('transactions:transaction_list')

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Обновляем баланс счета только если это новая транзакция
        # или изменилась сумма или счет
        if is_new:
            self.account.update_balance()