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


class SpamDetectionModel(models.Model):
    text = models.CharField(max_length=255)
    url = models.URLField(max_length=200)
    spam_not_spam = models.BooleanField()
    risk_associated = models.FloatField()

    def __str__(self):
        return self.text
    

class TransactionPatternDetectionModel(models.Model):
    sender_location = models.CharField(max_length=255)
    sender_device_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    sender_upi_ac_no = models.CharField(max_length=255)
    receiver_upi_ac_no = models.CharField(max_length=255)
    sender_acc_balance = models.DecimalField(max_digits=10, decimal_places=2)
    mode_of_transaction = models.CharField(max_length=255)
    frequency_of_transaction = models.IntegerField()
    fraud_not_fraud = models.BooleanField()

    def __str__(self):
        return f"{self.sender_device_id} to {self.receiver_upi_ac_no} - {self.amount}"


class TransactionModel(models.Model):
    TransactionID = models.CharField(max_length=255)
    CustomerID = models.CharField(max_length=255)
    CustomerDOB= models.DateField()
    CustGender = models.CharField(max_length=7)
    CustLocation = models.CharField(max_length=255)
    CustAccountBalance= models.FloatField()
    TransactionDate= models.DateField()
    TransactionTime = models.BigIntegerField()
    TransactionAmount = models.FloatField()

    def __str__(self):
        return f"Transaction {self.TransactionID} by Customer {self.CustomerID} on {self.TransactionDate}"
    
class CustomerAccount(models.Model):
    CustomerId = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    CreditScore = models.IntegerField()
    CustLocation = models.CharField(max_length=255)
    CustGender = models.CharField(max_length=7)
    CustAge = models.IntegerField()
    CustAccountBalance= models.FloatField()
    
    