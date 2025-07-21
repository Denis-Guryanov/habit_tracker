# flake8: noqa
from rest_framework import viewsets, permissions, filters, generics
from .models import Habit
from .serializers import HabitSerializer, RegisterSerializer

# Create your views here.


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["time", "place", "action"]

    def get_queryset(self):
        if self.request.query_params.get("public") == "true":
            return Habit.objects.filter(is_public=True).order_by("id")
        return Habit.objects.filter(user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []
