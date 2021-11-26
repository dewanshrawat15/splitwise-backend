from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Account, Transaction, TransactionActivity
from django.contrib.auth.models import User
from django.core import serializers
from django.forms.models import model_to_dict

import string
import random
import json

# Create your views here.
class FinanceAccount(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        account = Account.objects.filter(account_user = User.objects.get(id = request.user.id))
        if len(account) > 0:
            return Response({
                "account_identifier": account[0].account_identifier
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "An error occurred"
        }, status=status.HTTP_400_BAD_REQUEST)

class TransactionActivity(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = []
        transactions = Transaction.objects.filter(requested_by = Account.objects.get(account_user = User.objects.get(id = request.user.id)))
        for i in transactions:
            data.append(model_to_dict(i))
        print(data)
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            transaction = Transaction.objects.create(
                account = Account.objects.get(account_identifier = request.data["account"]),
                transaction_type = request.data["transaction_type"],
                percentage_split = request.data["percentage_split"],
                requested_amount = request.data["requested_amount"],
                requested_by = Account.objects.get(account_user = User.objects.get(id = request.user.id)),
                transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 32)).upper()
            )
            transaction.save()
            return Response({
                "message": "Transaction recorded successfully"
            }, status = status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "message": e
            }, status=status.HTTP_400_BAD_REQUEST)