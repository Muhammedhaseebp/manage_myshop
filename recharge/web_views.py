from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy

from .models import Recharge
from .forms import RechargeForm

class RechargeCreateView(LoginRequiredMixin,CreateView):
    model= Recharge
    form_class = RechargeForm
    template_name = "recharge/recharge_form.html"
    success_url = reverse_lazy("recharge-list")
class RechargeListView(LoginRequiredMixin,ListView):
    model = Recharge
    template_name = "recharge/recharge_list.html"
    context_object_name = "recharges"
    ordering = ['-date','-id']
