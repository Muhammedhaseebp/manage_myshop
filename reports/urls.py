from django.urls import path
from .views import report_by_date,monthly_report_pdf

urlpatterns = [
    path("report/", report_by_date, name="report"),
    path("monthly-pdf/",monthly_report_pdf,name="monthly-pdf"),
]