from django.db import models

# Create your models here.
class Expense(models.Model):
    EXPENSE_TYPE = (
        ("DIRECT","Direct Expense"),
        ("INDIRECT", "Indirect Expense"),
        ("FOOD","Food"),
    )

    date = models.DateField(auto_now_add=True)
    expense_name = models.CharField(max_length=100)
    expense_type = models.CharField(max_length=20,choices=EXPENSE_TYPE)
    amount = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.expense_name
