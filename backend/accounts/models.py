from django.db import models
import datetime
from django.utils import timezone
from users.models import User
# Create your models here.
class LockingSystemModel(models.Model):
    credit = models.BooleanField(default=False)
    debit = models.BooleanField(default=False)
    net_banking = models.BooleanField(default=False)
    upi = models.BooleanField(default=False)
    # banking_app = models.BooleanField(default=False)

    def __str__(self):
        return f"Locking System - Credit: {self.credit}, Debit: {self.debit}, Net Banking: {self.net_banking}, UPI: {self.upi}"
    


class CreditCardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=255)
    cvv = models.IntegerField()
    pin = models.CharField(max_length=4,null=True, blank=True)  # Add PIN field
    expiration_date = models.DateField()

class DebitCardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=255)
    cvv = models.IntegerField()
    expiration_date = models.DateField()
    pin = models.CharField(max_length=4,null=True, blank=True)  # Add PIN field

class NetBankingDetailsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)


class VirtualCreditCardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=255)
    cvv = models.IntegerField()
    expiration_date = models.DateField()
    pin = models.CharField(max_length=4,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null= True)  # Add timestamp

class VirtualDebitCardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=255)
    cvv = models.IntegerField()
    expiration_date = models.DateField()
    pin = models.CharField(max_length=4,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True , null= True)  # Add timestamp

class VirtualNetBankingDetailsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True, null= True)  # Add timestamp

class TransactionModel(models.Model):
    TransactionID = models.CharField(max_length=255)
    sender_phnno = models.IntegerField(default=1234)
    receiver_phno = models.IntegerField(default=1234)
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
    email = models.EmailField(max_length=255, default="defaultemail@email.com")
    phnno = models.IntegerField(null= True)
    CreditScore = models.IntegerField()
    CustLocation = models.CharField(max_length=255)
    CustGender = models.CharField(max_length=7)
    CustAge = models.IntegerField()
    CustAccountBalance= models.FloatField()


