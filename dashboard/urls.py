from django.urls import path

from .views import (
    home,
    subjects_page,
    delete_subject,
    tasks_page,
    routines_page,
    exams_page,
    notifications_page,
    expenses_page,
)


urlpatterns = [

    # HOME
    path(
        "home/",
        home,
        name="home"
    ),


    # SUBJECTS
    path(
        "subjects/",
        subjects_page,
        name="subjects_page"
    ),

    path(
        "subjects/<int:pk>/delete/",
        delete_subject,
        name="delete_subject"
    ),


    # TASKS
    path(
        "tasks/",
        tasks_page,
        name="tasks_page"
    ),


    # ROUTINES
    path(
        "routines/",
        routines_page,
        name="routines_page"
    ),


    # EXAMS
    path(
        "exams/",
        exams_page,
        name="exams_page"
    ),


    # NOTIFICATIONS
    path(
        "notifications/",
        notifications_page,
        name="notifications_page"
    ),


    # EXPENSES
    path(
        "expenses/",
        expenses_page,
        name="expenses_page"
    ),

]