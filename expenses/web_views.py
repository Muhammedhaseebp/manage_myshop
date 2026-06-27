from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy
from datetime import date

from .models import Expense
from .forms import ExpenseForm

class ExpenseCreateView(LoginRequiredMixin,CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expenses/expense_form.html"
    success_url = reverse_lazy("expense-list")
class ExpenseListView(LoginRequiredMixin,ListView):
    model = Expense
    template_name = "expenses/expense_list.html"
    context_object_name = "expenses"
    ordering = ['-date','-id']
    def get_queryset(self):
        today = date.today()
        return Expense.objects.filter(date=today).order_by('-id')

      