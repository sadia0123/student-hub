from rest_framework import serializers
from .models import Exam, Notification


class ExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = [
            "id",
            "subject",
            "exam_date",
            "exam_time",
            "room",
            "note",
        ]
class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
            "id",
            "message",
            "is_read",
            "created_at",
        ]        