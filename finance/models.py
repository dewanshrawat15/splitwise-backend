from django.db import models
from django.utils import timezone

# Create your models here.
class Account(models.Model):
    account_identifier = models.CharField(max_length = 16)
    account_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    account_created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.account_identifier

class Transaction(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name = 'creator')
    transaction_date_time = models.DateTimeField(default=timezone.now)
    transaction_type = models.CharField(max_length=6, choices=(("c", "CREDIT"), ("d", "DEBIT")))
    percentage_split = models.CharField(max_length=3)
    requested_amount = models.CharField(max_length=32)
    requested_by = models.ForeignKey('Account', on_delete=models.CASCADE, related_name = 'requester')
    transaction_status = models.CharField(max_length=15, choices=(("s", "SUCCESSFUL"), ("p", "PENDING")), default="PENDING")
    transaction_id = models.CharField(max_length=32)

    def __str__(self):
        return self.transaction_id

class TransactionActivity(models.Model):
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE, related_name='transaction_activity_id')
    transaction_activity_date_time = models.DateTimeField(default=timezone.now)
    transaction_amount = models.CharField(max_length=32)
    payee = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='payee_user')
    transaction_activity_identifier = models.CharField(max_length=20)

    def __str__(self):
        return self.transaction_activity_identifier