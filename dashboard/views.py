from django.shortcuts import render
from datetime import date
from decimal import Decimal

from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from sales.models import Sale
from recharge.models import Recharge
from expenses.models import Expense
from .models import DailyBalance

# Create your views here.
@extend_schema(tags=["Dashboard"],summary="Daily Dashboard Report",description="""Returns today's business summary.
Includes:Total Sales,Total Cash Payment,Total GPay Payment,Total Recharge,Today's Profit,Today's Indirect Expense,Opening Balance,Closing Balance
Formula
Today's Profit = Sales Profit + Recharge Profit
Closing Balance = Total Sales + Total Recharge − All Expenses
Opening Balance = Previous Day Closing Balance""")
class DailyDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        today = date.today()
        sales = Sale.objects.filter(date = today)
        recharge = Recharge.objects.filter(date = today)
        expenses = Expense.objects.filter(date = today)
        total_cash = (sales.filter(payment_method = "CASH").aggregate(total = Sum("amount"))["total"] or Decimal("0"))
        total_gpay = (sales.filter(payment_method = "GPAY").aggregate(total = Sum("amount"))["total"] or Decimal ("0"))
        total_sale = (sales.aggregate(total = Sum("amount"))["total"] or Decimal("0"))
        sales_profit = (sales.aggregate(total = Sum("profit")) ["total"] or Decimal("0"))
        recharge_total = (recharge.aggregate(total = Sum("total_recharge"))["total"] or Decimal("0"))
        recharge_profit = (recharge.aggregate(total = Sum("recharge_profit"))["total"] or Decimal("0"))
        direct_expense = (expenses.filter(expense_type = "DIRECT").aggregate(total = Sum("amount")) ["total"] or Decimal("0"))
        indirect_expense = (expenses.filter(expense_type = "INDIRECT").aggregate(total = Sum("amount"))["total"] or Decimal("0"))
        food_expense = (expenses.filter(expense_type = "FOOD").aggregate(total = Sum("amount"))["total"] or Decimal("0"))
        today_profit = (sales_profit + recharge_profit)
        today_indirect_expense = (indirect_expense + food_expense) 
        total_expense = (direct_expense + indirect_expense + food_expense)
        yesterday = DailyBalance.objects.order_by("-date").first()
        opening_balance = (yesterday.closing_balance if yesterday else Decimal("0"))
        closing_balance = (opening_balance + total_sale + recharge_total - total_expense)
        DailyBalance.objects.update_or_create(date = today,defaults={ 
            "opening_balance":opening_balance,"closing_balance":closing_balance})
        
        return Response({
            "opening_balance":opening_balance,
            "total_cash" : total_cash,
            "total_gpay" : total_gpay,
            "today_total_sale" : total_sale,
            "sales_profit" : sales_profit,
            "recharge_profit" : recharge_profit,
            "today_profit" : today_profit,
            "direct_expense" : direct_expense,
            "indirect_expense" : indirect_expense,
            "food_expense" : food_expense,
            "today_indirect_expense" : today_indirect_expense,
            "closing_balance" : closing_balance 


        })
from datetime import datetime

@extend_schema(tags=["Dashboard"],summary="Monthly Dashboard Report",description="""Returns monthly business report.
Includes Monthly Sales,Monthly Profit,Monthly Food Expense,Monthly Indirect Expense,Net Profit
Formula
Net Profit = Monthly Profit − Monthly Indirect Expense""")

class MonthlyDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        today = date.today()
        sales = Sale.objects.filter(date__year = today.year,date__month = today.month)
        recharge = Recharge.objects.filter(date__year = today.year,date__month = today.month)
        expenses = Expense.objects.filter(date__year = today.year,date__month = today.month)
        monthly_sale = (sales.aaggregate(total = Sum("amount"))["total"] or Decimal("0"))
        sales_profit = (sales.aaggregate(total = Sum("profit"))["total"] or Decimal("0"))
        recharge_profit = (recharge.aaggregate(total = Sum("recharge_profit"))["total"] or Decimal("0"))
        monthly_profit = (sales_profit + recharge_profit)
        monthly_food = (expenses.filter(expense_type = "FOOD").aggregate(total = Sum("amount")) ["total"] or Decimal("0"))
        monthly_indirect = (expenses.filter(expense_type ="INDIRECT").aggregate(total = Sum("amount")) ["total"] or Decimal("0"))
        monthly_indirect_expense = (monthly_indirect + monthly_food)
        net_profit = (monthly_profit - monthly_indirect_expense)

        return Response({
            "monthly_sale" : monthly_sale,
            "monthly_profit" : monthly_profit,
            "monthly_food" : monthly_food,
            "monthly_indirect_expense" : monthly_indirect_expense,
            "net_profit" : net_profit
        })
