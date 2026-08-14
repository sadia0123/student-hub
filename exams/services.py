from django.utils import timezone
from datetime import timedelta

from .models import Exam, Notification


def create_exam_notifications():

    today = timezone.localdate()
    tomorrow = today + timedelta(days=1)

    exams = Exam.objects.filter(
        exam_date=tomorrow
    )

    for exam in exams:

        message = (
            f"{exam.subject.name} exam is tomorrow "
            f"at {exam.exam_time}."
        )

        Notification.objects.get_or_create(
            user=exam.user,
            message=message
        )