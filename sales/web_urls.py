from django.urls import path
from .web_views import (SaleCreateView,SaleListView)

urlpatterns = [
    path("sales/add/",SaleCreateView.as_view(),name="sales-add"),
    path("sales/list/",SaleListView.as_view(),name="sales-list"),
   
]