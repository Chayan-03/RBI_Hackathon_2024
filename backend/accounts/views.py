from django.shortcuts import render
from rest_framework import generics, permissions
from .models import TransactionModel
from .serializers import TransactionSerializer

class UserTransactionsView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TransactionModel.objects.filter(sender_upi=user.upi_id)

