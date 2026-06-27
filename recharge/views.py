from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Recharge
from .serializer import RechargeSerializer
from accounts.permissions import (StaffNoEditDelete)

# Create your views here.
class RechargeViewSet(viewsets.ModelViewSet):
    queryset = Recharge.objects.all()
    serializer_class = RechargeSerializer
    permission_classes = [IsAuthenticated,StaffNoEditDelete]
