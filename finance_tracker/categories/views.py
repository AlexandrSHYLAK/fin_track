from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Category
from .forms import CategoryForm, CategoryFilterForm


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user)

        # Фильтрация по типу
        category_type = self.request.GET.get('type')
        if category_type:
            queryset = queryset.filter(type=category_type)

        # Поиск по названию
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset.order_by('type', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = CategoryFilterForm(self.request.GET or None)

        # Добавляем статистику
        user_categories = Category.objects.filter(user=self.request.user)
        context['total_categories'] = user_categories.count()
        context['income_categories_count'] = user_categories.filter(type='income').count()
        context['expense_categories_count'] = user_categories.filter(type='expense').count()

        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:category_list')

    def get_initial(self):
        initial = super().get_initial()
        # Получаем тип из GET-параметра
        category_type = self.request.GET.get('type')
        if category_type in ['income', 'expense']:
            initial['type'] = category_type
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Устанавливаем пользователя перед сохранением
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Категория успешно создана!')
        return response


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('categories:category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Категория успешно обновлена!')
        return response


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = reverse_lazy('categories:category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем другие категории пользователя для переназначения
        context['categories'] = Category.objects.filter(
            user=self.request.user
        ).exclude(id=self.object.id)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        new_category_id = request.POST.get('new_category_id')

        # Если есть транзакции и выбрана новая категория
        if self.object.transaction_set.exists() and new_category_id:
            try:
                new_category = Category.objects.get(id=new_category_id, user=request.user)
                # Переназначаем транзакции на новую категорию
                # Ленивый импорт для избежания циклической зависимости
                from transactions.models import Transaction
                Transaction.objects.filter(category=self.object).update(category=new_category)
            except Category.DoesNotExist:
                messages.error(request, 'Выбранная категория не найдена!')
                return self.render_to_response(self.get_context_data())

        messages.success(request, 'Категория успешно удалена!')
        return super().delete(request, *args, **kwargs)