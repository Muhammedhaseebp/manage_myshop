from django.db import models

# Create your models here.
class Recharge(models.Model):
    date = models.DateField(auto_now_add=True)
    total_recharge = models.DecimalField(max_digits=10,decimal_places=2)
    recharge_profit = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.date}"