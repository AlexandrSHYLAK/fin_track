from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Название категории',
            'type': 'Тип категории',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        initial_type = kwargs.pop('initial_type', None)

        super().__init__(*args, **kwargs)

        if initial_type:
            self.fields['type'].initial = initial_type


class CategoryFilterForm(forms.Form):
    type = forms.ChoiceField(
        choices=[('', 'Все типы'), ('income', 'Доход'), ('expense', 'Расход')],
        required=False,
        label='Тип категории',
        widget=forms.Select(attrs={'class': 'form-select'})
    )