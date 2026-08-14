from django.urls import path

from .views import (ExamListView, 
                    ExamDetailView,
                    NotificationListView,
                    CreateExamNotificationView,
                    NotificationDetailView)

urlpatterns = [

    path(
        "exams/",
        ExamListView.as_view()
    ),

    path(
        "exams/<int:pk>/",
        ExamDetailView.as_view()
    ),

    path(
        "notifications/",
        NotificationListView.as_view()
    ),
    path(
    "notifications/create/",
    CreateExamNotificationView.as_view()
),
path(
    "notifications/<int:pk>/",
    NotificationDetailView.as_view()
),

]