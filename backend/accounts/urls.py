from django.urls import path
from .views import UserTransactionsView,GenerateRandomCreditCardView, GenerateRandomDebitCardView, GenerateRandomNetBankingDetailsView


urlpatterns = [
    path('user-transactions/', UserTransactionsView.as_view(), name='user-transactions'),
    path('generate-random-credit-card/', GenerateRandomCreditCardView.as_view(), name='generate-random-credit-card'),
    path('generate-random-debit-card/', GenerateRandomDebitCardView.as_view(), name='generate-random-debit-card'),
    path('generate-random-net-banking/', GenerateRandomNetBankingDetailsView.as_view(), name='generate-random-net-banking'),
]
