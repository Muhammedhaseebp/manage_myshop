from django import forms
from .models import Sale

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = [
            "code",
            "product_name",
            "payment_method",
            "amount"
        ]