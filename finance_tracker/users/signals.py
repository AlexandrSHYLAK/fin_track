from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from categories.models import Category
from accounts.models import Account


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Создаем начальные категории для нового пользователя
        initial_categories = [
            {'name': 'Зарплата', 'type': 'income'},
            {'name': 'Подработка', 'type': 'income'},
            {'name': 'Подарки', 'type': 'income'},
            {'name': 'Еда', 'type': 'expense'},
            {'name': 'Транспорт', 'type': 'expense'},
            {'name': 'Развлечения', 'type': 'expense'},
            {'name': 'Коммунальные услуги', 'type': 'expense'},
            {'name': 'Здоровье', 'type': 'expense'},
        ]

        for cat_data in initial_categories:
            Category.objects.create(
                user=instance,
                name=cat_data['name'],
                type=cat_data['type']
            )

        # Создаем начальные счета
        initial_accounts = [
            {'name': 'Наличные'},
            {'name': 'Банковская карта'},
            {'name': 'Сберегательный счет'},
        ]

        for acc_data in initial_accounts:
            Account.objects.create(
                user=instance,
                name=acc_data['name'],
                balance=0
            )