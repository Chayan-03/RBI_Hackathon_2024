from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import Report, TransactionModel, VirtualDebitCardModel , VirtualCreditCardModel, CustomerAccount
from .serializers import ReportSerializer, TransactionSerializer, CreditCardSerializer, DebitCardSerializer, VirtualCreditCardSerializer, VirtualDebitCardSerializer
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
            credit_card = VirtualDebitCardModel.objects.create(
                user=user,
                cvv= generate_random_cvv(),
                card_number=generate_random_card_number(),
                card_holder_name=f'{user.name}',
                expiration_date=timezone.now().date() + timezone.timedelta(days=365*5),  # 5 years validity
                pin=generate_random_pin()  # Generate PIN
            )
            serializer = DebitCardSerializer(credit_card)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error generating credit card: {e}")
            logger.error(traceback.format_exc())
            return Response({'error': 'An error occurred while generating the credit card'}, status=500)
        
class ReportTransaction(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        transaction_id = request.data.get('transaction_id')
        description = request.data.get('description')
        image_1 = request.FILES.get('product_image_1', None)
        image_2 = request.FILES.get('product_image_2', None)

        # Find the transaction to get the receiver
        try:
            transaction = TransactionModel.objects.get(transaction_id=transaction_id)
            receiver = transaction.receiver
        except TransactionModel.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        report_details = {
            'transaction_id': transaction_id,
            'description': description,
            'image_1': image_1,
            'image_2': image_2,
            'receiver': receiver.id,
        }

        serializer = ReportSerializer(data=report_details)
        if serializer.is_valid():
            serializer.save()

            # Count the number of reports for the receiver
            report_count = Report.objects.filter(receiver=receiver).count()
            if report_count > 10:
                # Freeze the account
                customer_account = CustomerAccount.objects.get(CustomerId=receiver.id)
                customer_account.is_frozen = True  # Assuming you have a field 'is_frozen' to mark the account as frozen
                customer_account.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
