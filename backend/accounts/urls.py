from django.urls import path
from .views import UserTransactionsView

urlpatterns = [
    path('user-transactions/', UserTransactionsView.as_view(), name='user-transactions'),
]
