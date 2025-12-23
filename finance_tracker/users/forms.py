from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap ко всем полям
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label

        # Настраиваем тексты подсказок
        self.fields['username'].help_text = 'Обязательное поле. Не более 150 символов. Только буквы, цифры и @/./+/-/_'
        self.fields['password1'].help_text = '''
            <ul class="mb-0">
                <li>Пароль не должен быть слишком похож на другую вашу личную информацию.</li>
                <li>Ваш пароль должен содержать как минимум 8 символов.</li>
                <li>Пароль не должен быть слишком простым и распространенным.</li>
                <li>Пароль не может состоять только из цифр.</li>
            </ul>
        '''
        self.fields['password2'].help_text = 'Введите тот же пароль, что и выше, для проверки.'


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = 'Неверное имя пользователя или пароль.'