import json

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import NewUserSerializer

from rest_framework import status
from rest_framework.permissions import AllowAny

class UserRegistration(APIView):
    permission_classes = (AllowAny,)
    serializer_class = NewUserSerializer

    def post(self, request):
        serializer = NewUserSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Respones(serializer.errors, status = status.HTTP_400_BAD_REQUEST)