from django.shortcuts import render
from rest_framework import generics
from .serializers import UserRegisterSerializer
from .models import User

# Create your views here.

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []
