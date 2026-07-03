from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Sale
from .serializer import SaleSerializer
from accounts.permissions import (StaffNoEditDelete)
# Create your views here.
@extend_schema(tags =["Sales"],summary="Sales Management API",description=""" This API is used to manage sales.
               Features:Create Sale,View Sales,Update Sale(owner only),Delete Sale(owner only) 
               Profit is calculated automatically.
               code mapping:
               O = 0
               M = 1
               A = 2
               R = 3
               K = 4
               E = 5
               T = 6
               I = 7
               N = 8
               G = 9 
               Example:product code = MOO code Value = 100 Profit = Amount - 100""")

class SaleViewset(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by("-date")
    serializer_class = SaleSerializer
    permission_classes = [
        IsAuthenticated,
        StaffNoEditDelete
    ]
