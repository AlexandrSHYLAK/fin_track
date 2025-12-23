from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserLoginForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация прошла успешно! Теперь вы можете войти.')
        return response

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('transactions:transaction_list')
        return super().get(request, *args, **kwargs)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('transactions:transaction_list')

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                next_url = request.GET.get('next', 'transactions:transaction_list')
                return redirect(next_url)
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('users:login')


@login_required
def profile_view(request):
    # Получаем статистику пользователя
    from transactions.models import Transaction
    from accounts.models import Account
    from categories.models import Category

    total_transactions = Transaction.objects.filter(user=request.user).count()
    total_accounts = Account.objects.filter(user=request.user).count()
    total_categories = Category.objects.filter(user=request.user).count()

    # Последние транзакции
    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]

    context = {
        'user': request.user,
        'total_transactions': total_transactions,
        'total_accounts': total_accounts,
        'total_categories': total_categories,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'users/profile.html', context)
