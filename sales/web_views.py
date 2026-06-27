from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy

from django.http import HttpResponseForbidden
from django.shortcuts import render

from .models import Sale
from .forms import SaleForm

from datetime import date

class SaleCreateView(LoginRequiredMixin,CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "sales/sales_form.html"
    success_url = reverse_lazy("sales-list")

class SaleListView(LoginRequiredMixin,ListView):
    model = Sale
    template_name = "sales/sales_list.html"
    context_object_name = "sales"
    ordering = ['-date','-id']

    def get_queryset(self):
        today = date.today()
        return Sale.objects.filter(date=today).order_by('-id')

