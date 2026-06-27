from django import forms
from .models import Recharge

class RechargeForm(forms.ModelForm):
    class Meta:
        model = Recharge
        fields = [
            "total_recharge",
            "recharge_profit"
        ]