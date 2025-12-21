from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib import messages

from .models import Transaction
from .forms import TransactionForm, TransactionFilterForm


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        queryset = Transaction.objects.filter(
            user=self.request.user
        ).select_related('category', 'account')

        # Фильтрация по дате
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        category_id = self.request.GET.get('category')

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем форму фильтрации
        context['filter_form'] = TransactionFilterForm(
            self.request.GET or None,
            user=self.request.user
        )

        # Расчет сумм доходов и расходов
        queryset = self.get_queryset()
        income = queryset.filter(
            category__type='income'
        ).aggregate(total=Sum('amount'))['total'] or 0

        expense = queryset.filter(
            category__type='expense'
        ).aggregate(total=Sum('amount'))['total'] or 0

        context.update({
            'total_income': income,
            'total_expense': expense,
            'balance': income - expense,
        })

        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:transaction_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Транзакция успешно создана!')
        return super().form_valid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Транзакция успешно обновлена!')
        return super().form_valid(form)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transactions:transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Транзакция успешно удалена!')
        return super().delete(request, *args, **kwargs)