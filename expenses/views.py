from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Expense
from . serializer import ExpenseSerializer
from accounts.permissions import (StaffNoEditDelete)

# Create your views here.
@extend_schema(tags=["Expenses"],summary="Expense Management API",description="""This API manages all shop expenses.
Features:Create Expense,View Expense,Update Expense (Owner only),Delete Expense (Owner only)
Expense Types:1. Direct Expense 2. Indirect Expense 3. Food Expense
Business Rules
• Direct Expense:Used only for Closing Balance.
• Indirect Expense:Used for Monthly Net Profit calculation.
• Food Expense:Added to Today's Indirect Expense.
Formula
Today's Indirect Expense=Indirect Expense + Food
Closing Balance=Total Sales + Recharge - All Expenses
Net Profit = Monthly Profit - Total Indirect Expenses""",)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [
        IsAuthenticated,
        StaffNoEditDelete
    ]
