from decimal import Decimal
from django.db.models import Sum
from sales.models import Sale
from recharge.models import Recharge
from expenses.models import Expense

from .models import DailyBalance


def get_opening_balance(today):
    previous = (DailyBalance.objects.exclude(date = today).order_by("-date").first())

    if previous:
        return previous.closing_balance
    
    return Decimal("0")

def get_closing_balance(today):

    opening = get_opening_balance(today)
    total_sale = (Sale.objects.filter(date = today).aggregate(total = Sum("amount"))["total"] or Decimal("0"))
    total_recharge = (Recharge.objects.filter(date=today).aggregate(total=Sum("total_recharge"))["total"] or Decimal("0"))
    total_expense = (Expense.objects.filter(date=today).aggregate(total = Sum("amount"))["total"] or Decimal("0"))
    closing = (opening + total_sale + total_recharge - total_expense)

    return closing
def update_daily_balance(today,opening,closing):
    DailyBalance.objects.update_or_create(date = today,defaults={
        "opening_balance" : opening,"closing_balance": closing,

    })