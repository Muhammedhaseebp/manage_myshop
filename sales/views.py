from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Sale
from .serializer import SaleSerializer
from accounts.permissions import (StaffNoEditDelete)
# Create your views here.

class SaleViewset(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by("-date")
    serializer_class = SaleSerializer
    permission_classes = [
        IsAuthenticated,
        StaffNoEditDelete
    ]
