from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from .models import Recharge
from .serializer import RechargeSerializer
from accounts.permissions import (StaffNoEditDelete)

# Create your views here.
@extend_schema(tags = ["Recharge"],summary="Recharge API",description=""" This API manages recharge entries.Features:
               Create Recharge,View Recharge Record,Update Recharge(owner only),Delete Recharge (owner only)
               Recharge Profit is added to Today's Profit. Formula: Today's Profit = Sales Profit + Recharge Profit """)

class RechargeViewSet(viewsets.ModelViewSet):
    queryset = Recharge.objects.all()
    serializer_class = RechargeSerializer
    permission_classes = [IsAuthenticated,StaffNoEditDelete]
