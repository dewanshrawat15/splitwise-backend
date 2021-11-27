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
        try:
            account = Account.objects.filter(account_user = User.objects.get(id = request.user.id))
            if len(account) > 0:
                return Response({
                    "account_identifier": account[0].account_identifier
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "An error occurred"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": e
            }, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetail(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            data = []
            transactions = Transaction.objects.filter(requested_by = Account.objects.get(account_user = User.objects.get(id = request.user.id)), transaction_status = "p")
            for i in transactions:
                data.append(i.get_details())
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": e
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        try:
            transaction = Transaction.objects.create(
                account = Account.objects.get(account_identifier = request.data["account"]),
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

class TransactionActivities(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            to_payoff_transactions = Transaction.objects.filter(
                account = Account.objects.get(
                    account_user = User.objects.get(id = request.user.id)
                ),
                transaction_status = "p"
            )
            to_receive_transactions = Transaction.objects.filter(
                requested_by = Account.objects.get(
                    account_user = User.objects.get(id = request.user.id)
                ),
                transaction_status = "p"
            )
            to_payoff_list = []
            to_receive_list = []
            for i in to_payoff_transactions:
                transaction_activity_logs = TransactionActivity.objects.filter(
                    transaction = i
                )
                data = i.get_details()
                data["remaining_amount"] = int(i.requested_amount) - int(sum([i.transaction_amount for i in transaction_activity_logs]))
                data["account_holder"] = i.account.account_user.username
                to_payoff_list.append(data)
            for i in to_receive_transactions:
                transaction_activity_logs = TransactionActivity.objects.filter(
                    transaction = i
                )
                data = i.get_details()
                data["remaining_amount"] = int(i.requested_amount) - int(sum([i.transaction_amount for i in transaction_activity_logs]))
                data["account_holder"] = i.account.account_user.username
                to_receive_list.append(data)
            return Response({
                "receive_money": to_receive_list,
                "send_money": to_payoff_list
            }, status=HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": e
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        try:
            transaction_activity = TransactionActivity.objects.create(
                transaction = Transaction.objects.get(
                    transaction_id = request.data["transaction_id"]
                ),
                transaction_amount = request.data['amount'],
                payee = request.user,
                transaction_activity_identifier = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 32)).upper()
            )
            details = {
                "message": "Successful"
            }
            return Response(details, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": e
            }, status=status.HTTP_400_BAD_REQUEST)

class TransactionLogs(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            data = []
            transaction_activities = TransactionActivity.objects.filter(payee = request.user)
            for i in transaction_activities:
                data.append(i.get_details())
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": e
            }, status=status.HTTP_400_BAD_REQUEST)