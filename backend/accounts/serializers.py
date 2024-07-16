from rest_framework import serializers
from .models import Report, TransactionModel, LockingSystemModel, CreditCardModel , DebitCardModel, VirtualCreditCardModel , VirtualDebitCardModel 

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = '__all__'

class LockingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LockingSystemModel
        fields = '__all__'

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardModel
        fields = '__all__'

class DebitCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebitCardModel
        fields = '__all__'

class VirtualCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualCreditCardModel
        fields = '__all__'

class VirtualDebitCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualDebitCardModel
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


