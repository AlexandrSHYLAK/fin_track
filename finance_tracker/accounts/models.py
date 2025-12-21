from django.db import models
from django.conf import settings


class Account(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Название счета'
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Текущий баланс'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлен'
    )

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'
        ordering = ['name']
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.name} ({self.balance} ₽)"

    def update_balance(self):
        """Обновляет баланс счета на основе всех транзакций"""
        from transactions.models import Transaction

        total = Transaction.objects.filter(
            account=self
        ).aggregate(total=models.Sum('amount'))['total'] or 0

        if self.balance != total:
            self.balance = total
            self.save(update_fields=['balance'])