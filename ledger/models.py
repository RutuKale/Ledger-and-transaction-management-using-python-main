from django.db import models

class Ledger_tbl(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    LEDGER_CHOICES = [
        ('Given', 'Given'),
        ('Taken', 'Taken'),
    ]
    ledger = models.ForeignKey(Ledger_tbl, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    type = models.CharField(max_length=10, choices=LEDGER_CHOICES)
    created = models.DateTimeField(auto_now_add=True)  # Automatically set the field when the object is created
    updated = models.DateTimeField(auto_now=True)      # Automatically update the field every time the object is saved

    def __str__(self):
        return f"{self.ledger.name} - {self.amount} - {self.type}"
