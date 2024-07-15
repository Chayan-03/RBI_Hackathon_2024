from rest_framework import serializers
from .models import TransactionModel, LockingSystemModel

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionModel
        fields = '__all__'

class LockingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LockingSystemModel
        fields = '__all__'