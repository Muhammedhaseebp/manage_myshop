from django.db import models

# Create your models here.
PAYMENT_CHOICES = (
    ("CASH","Cash"),
    ("GPAY","GPay"),
)

class Sale(models.Model):
    date = models.DateField(auto_now_add=True)
    code = models.CharField(max_length=10)
    product_name = models.CharField(max_length=100,default="Unknown Product")
    code_value = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=10,choices=PAYMENT_CHOICES)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    profit = models.DecimalField(max_digits=10,decimal_places=2,default=0)


    def save(self, *args,**kwargs):

        mapping = {
            "O" : "0",
            "M" : "1",
            "A" : "2",
            "R" : "3",
            "K" : "4",
            "E" : "5",
            "T" : "6",
            "I" : "7",
            "N" : "8",
            "G" : "9",
        }

        product = self.code.upper()
        number = "".join(mapping.get(char, "")
                         for char in product)
        self.code_value = int(number)
        self.profit = self.amount - self.code_value

        super().save(*args, **kwargs)

    def __str__(self):
        return self.code