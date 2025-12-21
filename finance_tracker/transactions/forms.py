from django import forms
from .models import Transaction


class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'category', 'account', 'description']
        widgets = {
            'date': DateInput(),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'amount': 'Сумма',
            'date': 'Дата',
            'category': 'Категория',
            'account': 'Счет',
            'description': 'Описание',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Фильтруем категории и счета только текущего пользователя
            from categories.models import Category
            from accounts.models import Account

            self.fields['category'].queryset = Category.objects.filter(user=user)
            self.fields['account'].queryset = Account.objects.filter(user=user)

            # Устанавливаем пустое значение по умолчанию
            self.fields['category'].empty_label = 'Выберите категорию'
            self.fields['account'].empty_label = 'Выберите счет'


class TransactionFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=DateInput(),
        label='С'
    )
    end_date = forms.DateField(
        required=False,
        widget=DateInput(),
        label='По'
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label='Категория',
        empty_label='Все категории'
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            from categories.models import Category
            self.fields['category'].queryset = Category.objects.filter(user=user)