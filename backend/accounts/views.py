from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import TransactionModel, VirtualDebitCardModel , VirtualNetBankingDetailsModel, VirtualCreditCardModel
from .serializers import TransactionSerializer, CreditCardSerializer, DebitCardSerializer, NetBankingDetailsSerializer, VirtualCreditCardSerializer, VirtualDebitCardSerializer, VirtualNetBankingDetailsSerializer
import random
from datetime import date, time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_random_card_number, generate_random_account_number, generate_random_ifsc_code, generate_random_bank_name, generate_random_pin, generate_random_cvv
from apscheduler.schedulers.background import BackgroundScheduler
from users.models import User
from django.utils import timezone
import logging
import traceback



class UserTransactionsView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return TransactionModel.objects.filter(sender_phnno=user.phn)
# Configure logging
logger = logging.getLogger(__name__)

def delete_expired_data():
    expiration_time = timezone.now() - timezone.timedelta(minutes=5)
    VirtualCreditCardModel.objects.filter(created_at__lt=expiration_time).delete()
    VirtualDebitCardModel.objects.filter(created_at__lt=expiration_time).delete()
    VirtualNetBankingDetailsModel.objects.filter(created_at__lt=expiration_time).delete()

scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_data, 'interval', minutes=1)
scheduler.start()

class GenerateRandomCreditCardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            credit_card = VirtualCreditCardModel.objects.create(
                user=user,
                cvv= generate_random_cvv(),
                card_number=generate_random_card_number(),
                card_holder_name=f'{user.name}',
                expiration_date=timezone.now().date() + timezone.timedelta(days=365*5),  # 5 years validity
                pin=generate_random_pin()  # Generate PIN
            )
            serializer = CreditCardSerializer(credit_card)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error generating credit card: {e}")
            logger.error(traceback.format_exc())
            return Response({'error': 'An error occurred while generating the credit card'}, status=500)

class GenerateRandomDebitCardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            debit_card = VirtualDebitCardModel.objects.create(
                user=user,
                card_number=generate_random_card_number(),
                cvv= generate_random_cvv(),
                card_holder_name=f'{user.first_name} {user.last_name}',
                expiration_date=timezone.now().date() + timezone.timedelta(days=365*5),  # 5 years validity
                pin=generate_random_pin()  # Generate PIN
            )
            serializer = DebitCardSerializer(debit_card)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error generating debit card: {e}")
            return Response({'error': 'An error occurred while generating the debit card'}, status=500)

class GenerateRandomNetBankingDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            net_banking = VirtualNetBankingDetailsModel.objects.create(
                user=user,
                bank_name=generate_random_bank_name(),
                account_number=generate_random_account_number(),
                ifsc_code=generate_random_ifsc_code(),
                # pin=generate_random_pin()  # Generate PIN
            )
            serializer = NetBankingDetailsSerializer(net_banking)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error generating net banking details: {e}")
            return Response({'error': 'An error occurred while generating the net banking details'}, status=500)