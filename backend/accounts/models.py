from django.db import models
import datetime
# Create your models here.
class LockingSystemModel(models.Model):
    credit = models.BooleanField(default=False)
    debit = models.BooleanField(default=False)
    net_banking = models.BooleanField(default=False)
    upi = models.BooleanField(default=False)
    banking_app = models.BooleanField(default=False)

    def __str__(self):
        return f"Locking System - Credit: {self.credit}, Debit: {self.debit}, Net Banking: {self.net_banking}, UPI: {self.upi}, Banking App: {self.banking_app}"




class TransactionModel(models.Model):
    TransactionID = models.CharField(max_length=255)
    sender_upi = models.CharField(max_length=255, default='default_upi')
    receiver_upi = models.CharField(max_length=255, default='default_upi')
    CustomerID = models.CharField(max_length=255)
    CustomerDOB = models.DateField()
    CustGender = models.CharField(max_length=7)
    CustLocation = models.CharField(max_length=255)
    CustAccountBalance = models.FloatField()
    TransactionDate = models.DateField()
    TransactionTime = models.BigIntegerField()
    TransactionAmount = models.FloatField()

    def __str__(self):
        return f"Transaction {self.TransactionID} by Customer {self.CustomerID} on {self.TransactionDate}"
    def get_transaction_datetime(self):
        """
        Convert Unix timestamp to datetime.
        """
        return datetime.datetime.fromtimestamp(self.TransactionTime)
    
class CustomerAccount(models.Model):
    CustomerId = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    CreditScore = models.IntegerField()
    CustLocation = models.CharField(max_length=255)
    CustGender = models.CharField(max_length=7)
    CustAge = models.IntegerField()
    CustAccountBalance= models.FloatField()

    