from django.contrib import admin
from .models import LockingSystemModel, TransactionModel, CustomerAccount, CreditCardModel, DebitCardModel , NetBankingDetailsModel

admin.site.register(LockingSystemModel)
admin.site.register(TransactionModel)
admin.site.register(CustomerAccount)
admin.site.register(CreditCardModel)
admin.site.register(DebitCardModel)
admin.site.register(NetBankingDetailsModel)