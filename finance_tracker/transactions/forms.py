from django import forms
from .models import Transaction


class DateInput(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d'


class TransactionForm(forms.ModelForm):
    new_category_name = forms.CharField(
        max_length=100,
        required=False,
        label='Новая категория',
        help_text='Создать новую категорию (оставьте пустым, если выбрана существующая)',
        widget=forms.TextInput(attrs={'placeholder': 'Введите название новой категории'})
    )
    new_category_type = forms.ChoiceField(
        choices=[('', 'Выберите тип'), ('income', 'Доход'), ('expense', 'Расход')],
        required=False,
        label='Тип новой категории',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'category', 'account', 'description']
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'account': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'amount': 'Сумма',
            'date': 'Дата',
            'category': 'Категория',
            'account': 'Счет',
            'description': 'Описание',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            # Используем ленивые импорты
            from categories.models import Category
            from accounts.models import Account

            self.fields['category'].queryset = Category.objects.filter(user=self.user)
            self.fields['account'].queryset = Account.objects.filter(user=self.user)
            self.fields['category'].empty_label = 'Выберите категорию или создайте новую'

    def clean(self):
        cleaned_data = super().clean()
        new_category_name = cleaned_data.get('new_category_name')
        new_category_type = cleaned_data.get('new_category_type')
        category = cleaned_data.get('category')

        # Проверяем, что либо выбрана существующая категория, либо создана новая
        if not category and (not new_category_name or not new_category_type):
            raise forms.ValidationError(
                'Выберите существующую категорию или создайте новую (укажите название и тип).'
            )

        if new_category_name and new_category_type:
            # Проверяем, не существует ли уже такая категория
            from categories.models import Category
            if Category.objects.filter(user=self.user, name=new_category_name).exists():
                raise forms.ValidationError(
                    f'Категория "{new_category_name}" уже существует.'
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_category_name = self.cleaned_data.get('new_category_name')
        new_category_type = self.cleaned_data.get('new_category_type')

        if new_category_name and new_category_type:
            # Создаем новую категорию
            from categories.models import Category
            category = Category.objects.create(
                user=self.user,
                name=new_category_name,
                type=new_category_type
            )
            instance.category = category

        if commit:
            instance.save()

        return instance


class TransactionFilterForm(forms.Form):
    start_date = forms.DateField(
        required=False,
        widget=DateInput(attrs={'class': 'form-control'}),
        label='С'
    )
    end_date = forms.DateField(
        required=False,
        widget=DateInput(attrs={'class': 'form-control'}),
        label='По'
    )
    category = forms.ChoiceField(
        choices=[],
        required=False,
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            from categories.models import Category
            categories = Category.objects.filter(user=user)
            self.fields['category'].choices = [('', 'Все категории')] + [(c.id, c.name) for c in categories]