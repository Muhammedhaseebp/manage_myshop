from django.urls import path
from .web_views import (RechargeCreateView,RechargeListView)

urlpatterns =[
    path("recharge/add/",RechargeCreateView.as_view(),name="recharge-add"),
    path("recharge/list/",RechargeListView.as_view(),name="recharge-list"),
    
]