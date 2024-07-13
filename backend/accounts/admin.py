from django.contrib import admin
from .models import LockingSystemModel, SpamDetectionModel, TransactionPatternDetectionModel, TransactionModel, CustomerAccount

admin.site.register(LockingSystemModel)
admin.site.register(SpamDetectionModel)
admin.site.register(TransactionPatternDetectionModel)
admin.site.register(TransactionModel)
admin.site.register(CustomerAccount)
