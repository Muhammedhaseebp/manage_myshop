from django.urls import path
from .views import (DailyDashboardAPIView,MonthlyDashboardAPIView)

urlpatterns = [
    path("dashboard/daily/",DailyDashboardAPIView.as_view()),
    path("dashboard/monthly/",MonthlyDashboardAPIView.as_view()),
]
