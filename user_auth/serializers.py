from rest_framework import serializers
from django.contrib.auth.models import User

from finance.serializers import AccountSerializer
import string
import random

class NewUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password',)
        extra_kwargs = {"password":{'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        gen_account_identifier = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 16)).upper()
        acc_user_serializer = AccountSerializer(data = {'account_user': user.id, 'account_identifier': gen_account_identifier})
        if acc_user_serializer.is_valid(raise_exception=True):
            acc_user_serializer.save()
        return user