from django.contrib import admin
from .models import Account, Transaction, TransactionActivity
# Register your models here.
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(TransactionActivity)