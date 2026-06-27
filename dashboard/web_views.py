from datetime import date
from decimal import Decimal
from django.db.models import Sum

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from sales.models import Sale
from recharge.models import Recharge
from expenses.models import Expense
from accounts.decorators import (owner_required)

from .services import get_opening_balance,get_closing_balance,update_daily_balance

@owner_required
@login_required
def daily_dashboard(request):
    today = date.today()
    opening_balance = get_opening_balance(today)
    closing_balance = get_closing_balance(today)

    update_daily_balance(
        today,
        opening_balance,
        closing_balance
    )
    sales = Sale.objects.filter(date=today)
    expenses = Expense.objects.filter(date=today)
    total_sale = sum(s.amount for s in Sale.objects.filter(date=today))
    total_profit = sum(s.profit for s in Sale.objects.filter(date=today))
    recharge_profit = sum(r.recharge_profit for r in Recharge.objects.filter(date = today))

    context = {
        "today_total_sale" : total_sale,
        "today_profit" : total_profit + recharge_profit,
        "opening_balance":opening_balance,
        "total_cash": 0,
        "total_gpay": 0,
        "closing_balance" : closing_balance,
        "sales":sales,
        "expenses":expenses,

    }
    

    return render(request,"dashboard/daily.html",context,)

@login_required
@owner_required
def monthly_dashboard(request):
    today = date.today()
    sales = Sale.objects.filter(date__month = today.month,date__year=today.year)
    recharge = Recharge.objects.filter(date__month =today.month,date__year = today.year)
    expenses = Expense.objects.filter(date__month = today.month,date__year= today.year)
    monthly_sale =(sales.aggregate(total=Sum("amount"))["total"] or Decimal("0"))
    sales_profit = (sales.aggregate(total = Sum("profit"))["total"] or Decimal("0"))
    recharge_profit = (recharge.aggregate(total=Sum("recharge_profit"))["total"] or Decimal("0"))
    monthly_profit = (sales_profit + recharge_profit)
    monthly_food = (expenses.filter(expense_type = "FOOD").aggregate(total=Sum("amount"))["total"] or Decimal("0"))
    indirect = (expenses.filter(expense_type = "INDIRECT").aggregate(total=Sum("amount"))["total"] or Decimal('0'))
    monthly_indirect_expense = (indirect + monthly_food)
    net_profit = (monthly_profit - monthly_indirect_expense)

    return render(request,"dashboard/monthly.html",{
        "monthly_sale" : monthly_sale,
        "monthly_profit" : monthly_profit,
        "monthly_food" : monthly_food,
        "monthly_indirect_expense" : monthly_indirect_expense,
        "net_profit" : net_profit

    })
