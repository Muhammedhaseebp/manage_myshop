from django.db import models

# Create your models here.
class DailyBalance(models.Model):
    date = models.DateField(unique=True)
    opening_balance = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    closing_balance = models.DecimalField(max_digits=12,decimal_places=2,default=0)

    def __str__(self):
        return str(self.date)
