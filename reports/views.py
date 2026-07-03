from django.shortcuts import render

from datetime import datetime
from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal

from sales.models import Sale
from recharge.models import Recharge
from expenses.models import Expense

from .decorators import owner_or_superuser_required

from django.http import HttpResponse
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet




@login_required
@owner_or_superuser_required
def report_by_date(request):

    start = request.GET.get("start")
    end = request.GET.get("end")

    sales = Sale.objects.none()
    expenses = Expense.objects.none()
    recharge = Recharge.objects.none()

    total_sale = Decimal("0")
    total_profit = Decimal("0")
    recharge_profit = Decimal("0")
    total_expense = Decimal("0")

    if start and end:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()

        sales = Sale.objects.filter(date__range=[start_date, end_date])
        expenses = Expense.objects.filter(date__range=[start_date, end_date])
        recharge = Recharge.objects.filter(date__range=[start_date, end_date])

        total_sale = sales.aggregate(total=Sum("amount"))["total"] or Decimal("0")
        total_profit = sales.aggregate(total=Sum("profit"))["total"] or Decimal("0")
        recharge_profit = recharge.aggregate(total=Sum("recharge_profit"))["total"] or Decimal("0")
        total_expense = expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0")

    net_profit = (total_profit + recharge_profit) - total_expense

    return render(request, "reports/range_report.html", {
        "sales": sales,
        "expenses": expenses,
        "recharges": recharge,

        "total_sale": total_sale,
        "total_profit": total_profit + recharge_profit,
        "total_expense": total_expense,
        "net_profit": net_profit,

        "start": start,
        "end": end,
    })


@login_required
@owner_or_superuser_required
def monthly_report_pdf(request):

    today = date.today()

    # DATA
    sales = Sale.objects.filter(
        date__month=today.month,
        date__year=today.year
    )

    recharges = Recharge.objects.filter(
        date__month=today.month,
        date__year=today.year
    )

    expenses = Expense.objects.filter(
        date__month=today.month,
        date__year=today.year
    )

    food_expenses = expenses.filter(expense_type="FOOD")
    indirect_expenses = expenses.filter(expense_type="INDIRECT")

    # TOTALS
    total_sale = sales.aggregate(total=Sum("amount"))["total"] or Decimal("0")
    sales_profit = sales.aggregate(total=Sum("profit"))["total"] or Decimal("0")
    recharge_profit = recharges.aggregate(total=Sum("recharge_profit"))["total"] or Decimal("0")

    food_total = food_expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0")
    indirect_total = indirect_expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0")
    total_expense = expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0")

    net_profit = (sales_profit + recharge_profit) - (indirect_total + food_total)

    # RESPONSE
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="monthly_report.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    elements = []

    # TITLE
    elements.append(
        Paragraph(f"Monthly Report - {today.strftime('%B %Y')}", styles["Title"])
    )

    elements.append(Spacer(1, 20))

    # SUMMARY
    elements.append(Paragraph(f"Total Sale : ₹ {total_sale}", styles["Normal"]))
    elements.append(Paragraph(f"Sales Profit : ₹ {sales_profit}", styles["Normal"]))
    elements.append(Paragraph(f"Recharge Profit : ₹ {recharge_profit}", styles["Normal"]))
    elements.append(Paragraph(f"Food Expense : ₹ {food_total}", styles["Normal"]))
    elements.append(Paragraph(f"Indirect Expense : ₹ {indirect_total}", styles["Normal"]))
    elements.append(Paragraph(f"Total Expense : ₹ {total_expense}", styles["Normal"]))
    elements.append(Paragraph(f"Net Profit : ₹ {net_profit}", styles["Normal"]))

    elements.append(Spacer(1, 20))

    # =====================
    # SALES TABLE
    # =====================
    elements.append(Paragraph("Sales Details", styles["Heading2"]))

    sales_data = [["Date", "Product", "Payment", "Amount", "Profit"]]

    for s in sales:
        sales_data.append([
            str(s.date),
            s.product_name,
            s.payment_method,
            str(s.amount),
            str(s.profit),
        ])

    sales_table = Table(sales_data)

    sales_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    elements.append(sales_table)

    elements.append(Spacer(1, 20))

    # =====================
    # INDIRECT EXPENSE TABLE
    # =====================
    elements.append(Paragraph("Indirect Expense Details", styles["Heading2"]))

    indirect_data = [["Date", "Name", "Amount"]]

    for e in indirect_expenses:
        indirect_data.append([
            str(e.date),
            e.expense_name,
            str(e.amount),
        ])

    indirect_table = Table(indirect_data)

    indirect_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    elements.append(indirect_table)

    elements.append(Spacer(1, 20))

    # =====================
    # FOOD EXPENSE TABLE
    # =====================
    elements.append(Paragraph("Food Expense Details", styles["Heading2"]))

    food_data = [["Date", "Name", "Amount"]]

    for e in food_expenses:
        food_data.append([
            str(e.date),
            e.expense_name,
            str(e.amount),
        ])

    food_table = Table(food_data)

    food_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    elements.append(food_table)

    # BUILD PDF
    doc.build(elements)

    return response