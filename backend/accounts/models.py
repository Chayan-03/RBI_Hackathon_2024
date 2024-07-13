from django.db import models

# Create your models here.
class LockingSystemModel(models.Model):
    credit = models.BooleanField(default=False)
    debit = models.BooleanField(default=False)
    net_banking = models.BooleanField(default=False)
    upi = models.BooleanField(default=False)
    banking_app = models.BooleanField(default=False)

    def __str__(self):
        return f"Locking System - Credit: {self.credit}, Debit: {self.debit}, Net Banking: {self.net_banking}, UPI: {self.upi}, Banking App: {self.banking_app}"

