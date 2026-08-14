from django.core.management.base import BaseCommand

from exams.services import create_exam_notifications


class Command(BaseCommand):

    help = "Create notifications for exams happening tomorrow"

    def handle(self, *args, **kwargs):

        create_exam_notifications()

        self.stdout.write(
            self.style.SUCCESS(
                "Exam notifications checked successfully."
            )
        )