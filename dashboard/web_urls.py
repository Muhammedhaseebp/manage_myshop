from django.urls import path
from .web_views import (daily_dashboard,monthly_dashboard)

urlpatterns = [
    path("dashboard/daily/",daily_dashboard,name="daily-dashboard"),
    path("dashboard/monthly/",monthly_dashboard,name="monthly-dashboard"),
    
]