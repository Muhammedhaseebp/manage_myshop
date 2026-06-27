from django.urls import path
from .web_views import (ExpenseCreateView,ExpenseListView)

urlpatterns = [
    path("expense/add/",ExpenseCreateView.as_view(),name="expense-add"),
    path("expense/list/",ExpenseListView.as_view(),name="expense-list")
]