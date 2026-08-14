from django.urls import path

from .views import (
    SubjectListView,
    TaskDetailView,
    TaskListView,
    RoutineListView,
    RoutineDetailView,
)


urlpatterns = [

    path(
        "subjects/",
        SubjectListView.as_view()
    ),

    path(
        "tasks/",
        TaskListView.as_view()
    ),

    path(
        "tasks/<int:pk>/",
        TaskDetailView.as_view()
    ),

    path(
        "routines/",
        RoutineListView.as_view()
    ),

    path(
        "routines/<int:pk>/",
        RoutineDetailView.as_view()
    ),
]