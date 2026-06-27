from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Expense
from . serializer import ExpenseSerializer
from accounts.permissions import (StaffNoEditDelete)

# Create your views here.

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [
        IsAuthenticated,
        StaffNoEditDelete
    ]
