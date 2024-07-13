from django.contrib import admin
from .models import LockingSystemModel, SpamDetectionModel, TransactionPatternDetectionModel

admin.site.register(LockingSystemModel)
admin.site.register(SpamDetectionModel)
admin.site.register(TransactionPatternDetectionModel)


