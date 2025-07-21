from django.shortcuts import render
from rest_framework import generics

from .models import User
from .serializers import UserRegisterSerializer

# Create your views here.


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []
