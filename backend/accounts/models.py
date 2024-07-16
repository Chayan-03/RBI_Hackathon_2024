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
    pin = models.CharField(max_length=4, null=True, blank=True)  # Add PIN field
    expiration_date = models.DateField()

    def __str__(self):
        return f"Credit Card {self.card_number} for {self.card_holder_name}"


class DebitCardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=255)
    cvv = models.IntegerField()
    expiration_date = models.DateField()
    pin = models.CharField(max_length=4, null=True, blank=True)  # Add PIN field

    def __str__(self):
        return f"Debit Card {self.card_number} for {self.card_holder_name}"


class NetBankingDetailsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    ifsc_code = models.CharField(max_length=20)

    def __str__(self):
        return f"Net Banking Details for {self.bank_name}"


class VirtualCreditCardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=255)
    cvv = models.IntegerField()
    expiration_date = models.DateField()
    pin = models.CharField(max_length=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Add timestamp

    def __str__(self):
        return f"Virtual Credit Card {self.card_number} for {self.card_holder_name}"


class VirtualDebitCardModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder_name = models.CharField(max_length=255)
    cvv = models.IntegerField()
    expiration_date = models.DateField()
    pin = models.CharField(max_length=4, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Add timestamp

    def __str__(self):
        return f"Virtual Debit Card {self.card_number} for {self.card_holder_name}"


class TransactionModel(models.Model):
    transaction_id = models.CharField(max_length=255)
    sender_phnno = models.IntegerField(default=1234)
    receiver_phno = models.IntegerField(default=1234)
    customer_id = models.CharField(max_length=255)
    customer_dob = models.DateField()
    customer_gender = models.CharField(max_length=7)
    customer_location = models.CharField(max_length=255)
    customer_account_balance = models.FloatField()
    transaction_date = models.DateField()
    transaction_time = models.BigIntegerField()
    transaction_amount = models.FloatField()
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, default="1")

    def __str__(self):
        return f"Transaction {self.transaction_id} by Customer {self.customer_id} on {self.transaction_date}"

    def get_transaction_datetime(self):
        """
        Convert Unix timestamp to datetime.
        """
        return datetime.datetime.fromtimestamp(self.transaction_time)


class CustomerAccount(models.Model):
    customer_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, default="defaultemail@email.com")
    phnno = models.IntegerField(null=True)
    credit_score = models.IntegerField()
    customer_location = models.CharField(max_length=255)
    customer_gender = models.CharField(max_length=7)
    customer_age = models.IntegerField()
    customer_account_balance = models.FloatField()
    is_frozen = models.BooleanField(default=False)

    def __str__(self):
        return f"Customer Account {self.customer_id} - {self.name}"


class Report(models.Model):
    transaction_id = models.CharField(max_length=100)
    description = models.TextField()
    image_1 = models.ImageField(upload_to='images/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='images/', null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,default="1")

    def __str__(self):
        return f"Report for Transaction {self.transaction_id}"
