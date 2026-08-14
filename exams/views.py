from django.shortcuts import render

# Create your views here.
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .models import Exam, Notification
from .serializers import ExamSerializer, NotificationSerializer


class ExamListView(ListCreateAPIView):

    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Exam.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class ExamDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Exam.objects.filter(
            user=self.request.user
        )
    
class NotificationListView(ListAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        ).order_by("-created_at")


  
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import create_exam_notifications


class CreateExamNotificationView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        create_exam_notifications()

        return Response({
            "message": "Exam notifications checked successfully."
        })    

    
class NotificationDetailView(RetrieveUpdateAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )    