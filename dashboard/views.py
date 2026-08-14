from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime

from study.models import Subject, Task, Routine
from exams.models import Exam, Notification
from expenses.models import Expense, MonthlyBudget


# =========================================================
# HOME
# =========================================================

@login_required
def home(request):

    today = timezone.localdate()

    month = today.month
    year = today.year

    # Subjects
    subject_count = Subject.objects.filter(
        user=request.user
    ).count()

    # Exams
    upcoming_exams = Exam.objects.filter(
        user=request.user,
        exam_date__gte=today
    ).select_related(
        "subject"
    ).order_by(
        "exam_date",
        "exam_time"
    )

    next_exam = upcoming_exams.first()

    # Tasks
    pending_tasks = Task.objects.filter(
        subject__user=request.user,
        completed=False
    ).select_related(
        "subject"
    ).order_by(
        "deadline"
    )

    next_task = pending_tasks.first()

    # Expenses
    expenses = Expense.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    )

    monthly_expense = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    # Budget
    budget = MonthlyBudget.objects.filter(
        user=request.user,
        month=month,
        year=year
    ).first()

    monthly_budget = budget.amount if budget else 0

    remaining_budget = monthly_budget - monthly_expense

    # Notifications
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by(
        "-created_at"
    )

    context = {
        "subject_count": subject_count,

        "upcoming_exam_count": upcoming_exams.count(),
        "next_exam": next_exam,

        "pending_task_count": pending_tasks.count(),
        "next_task": next_task,

        "monthly_expense": monthly_expense,
        "monthly_budget": monthly_budget,
        "remaining_budget": remaining_budget,

        "unread_notification_count": notifications.count(),
        "latest_notification": notifications.first(),
    }

    return render(
        request,
        "home.html",
        context
    )


# =========================================================
# SUBJECTS
# =========================================================

@login_required
def subjects_page(request):

    if request.method == "POST":

        name = request.POST.get("name")
        code = request.POST.get("code")
        teacher = request.POST.get("teacher")

        if name:

            Subject.objects.create(
                user=request.user,
                name=name,
                code=code,
                teacher=teacher
            )

        return redirect("subjects_page")

    subjects = Subject.objects.filter(
        user=request.user
    ).order_by("name")

    return render(
        request,
        "subjects.html",
        {
            "subjects": subjects
        }
    )


@login_required
def delete_subject(request, pk):

    subject = get_object_or_404(
        Subject,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":
        subject.delete()

    return redirect("subjects_page")


# =========================================================
# TASKS
# =========================================================

@login_required
def tasks_page(request):

    subjects = Subject.objects.filter(
        user=request.user
    ).order_by("name")

    if request.method == "POST":

        action = request.POST.get("action")

        # ADD TASK
        if action == "add":

            subject_id = request.POST.get("subject")
            title = request.POST.get("title")
            description = request.POST.get("description")
            deadline = request.POST.get("deadline")

            subject = get_object_or_404(
                Subject,
                id=subject_id,
                user=request.user
            )

            deadline_value = None

            if deadline:

                deadline_value = datetime.fromisoformat(
                    deadline
                )

                if timezone.is_naive(deadline_value):

                    deadline_value = timezone.make_aware(
                        deadline_value
                    )

            Task.objects.create(
                subject=subject,
                title=title,
                description=description,
                deadline=deadline_value,
                completed=False
            )

        # COMPLETE / UNCOMPLETE
        elif action == "toggle":

            task_id = request.POST.get("task_id")

            task = get_object_or_404(
                Task,
                id=task_id,
                subject__user=request.user
            )

            task.completed = not task.completed

            task.save()

        # DELETE
        elif action == "delete":

            task_id = request.POST.get("task_id")

            task = get_object_or_404(
                Task,
                id=task_id,
                subject__user=request.user
            )

            task.delete()

        return redirect("tasks_page")

    tasks = Task.objects.filter(
        subject__user=request.user
    ).select_related(
        "subject"
    ).order_by(
        "completed",
        "deadline"
    )

    return render(
        request,
        "tasks.html",
        {
            "tasks": tasks,
            "subjects": subjects
        }
    )


# =========================================================
# ROUTINES
# =========================================================

@login_required
def routines_page(request):

    subjects = Subject.objects.filter(
        user=request.user
    ).order_by("name")

    if request.method == "POST":

        action = request.POST.get("action")

        # ADD ROUTINE
        if action == "add":

            subject_id = request.POST.get("subject")
            day = request.POST.get("day")
            start_time = request.POST.get("start_time")
            end_time = request.POST.get("end_time")
            room = request.POST.get("room")

            subject = get_object_or_404(
                Subject,
                id=subject_id,
                user=request.user
            )

            Routine.objects.create(
                subject=subject,
                day=day,
                start_time=start_time,
                end_time=end_time,
                room=room
            )

        # DELETE ROUTINE
        elif action == "delete":

            routine_id = request.POST.get("routine_id")

            routine = get_object_or_404(
                Routine,
                id=routine_id,
                subject__user=request.user
            )

            routine.delete()

        return redirect("routines_page")

    routines = Routine.objects.filter(
        subject__user=request.user
    ).select_related(
        "subject"
    ).order_by(
        "day",
        "start_time"
    )

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    return render(
        request,
        "routines.html",
        {
            "routines": routines,
            "subjects": subjects,
            "days": days
        }
    )


# =========================================================
# EXAMS
# =========================================================

@login_required
def exams_page(request):

    subjects = Subject.objects.filter(
        user=request.user
    ).order_by("name")

    if request.method == "POST":

        action = request.POST.get("action")

        # ADD EXAM
        if action == "add":

            subject_id = request.POST.get("subject")
            exam_date = request.POST.get("exam_date")
            exam_time = request.POST.get("exam_time")
            room = request.POST.get("room")
            note = request.POST.get("note")

            subject = get_object_or_404(
                Subject,
                id=subject_id,
                user=request.user
            )

            Exam.objects.create(
                user=request.user,
                subject=subject,
                exam_date=exam_date,
                exam_time=exam_time,
                room=room,
                note=note
            )

        # DELETE EXAM
        elif action == "delete":

            exam_id = request.POST.get("exam_id")

            exam = get_object_or_404(
                Exam,
                id=exam_id,
                user=request.user
            )

            exam.delete()

        return redirect("exams_page")

    exams = Exam.objects.filter(
        user=request.user
    ).select_related(
        "subject"
    ).order_by(
        "exam_date",
        "exam_time"
    )

    return render(
        request,
        "exams.html",
        {
            "exams": exams,
            "subjects": subjects
        }
    )


# =========================================================
# NOTIFICATIONS
# =========================================================

@login_required
def notifications_page(request):

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "read":

            notification_id = request.POST.get(
                "notification_id"
            )

            notification = get_object_or_404(
                Notification,
                id=notification_id,
                user=request.user
            )

            notification.is_read = True
            notification.save()

        elif action == "read_all":

            Notification.objects.filter(
                user=request.user,
                is_read=False
            ).update(
                is_read=True
            )

        return redirect("notifications_page")

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "notifications.html",
        {
            "notifications": notifications
        }
    )


# =========================================================
# EXPENSES
# =========================================================

@login_required
def expenses_page(request):

    today = timezone.localdate()

    month = today.month
    year = today.year

    if request.method == "POST":

        action = request.POST.get("action")

        # ADD EXPENSE
        if action == "add":

            amount = request.POST.get("amount")
            category = request.POST.get("category")
            description = request.POST.get("description")
            date = request.POST.get("date")

            Expense.objects.create(
                user=request.user,
                amount=amount,
                category=category,
                description=description,
                date=date
            )

        # DELETE EXPENSE
        elif action == "delete":

            expense_id = request.POST.get("expense_id")

            expense = get_object_or_404(
                Expense,
                id=expense_id,
                user=request.user
            )

            expense.delete()

        # SET BUDGET
        elif action == "budget":

            amount = request.POST.get("budget_amount")

            budget, created = MonthlyBudget.objects.get_or_create(
                user=request.user,
                month=month,
                year=year,
                defaults={
                    "amount": amount
                }
            )

            if not created:

                budget.amount = amount
                budget.save()

        return redirect("expenses_page")

    # Current month's expenses

    expenses = Expense.objects.filter(
        user=request.user,
        date__month=month,
        date__year=year
    ).order_by(
        "-date",
        "-created_at"
    )

    # Total

    monthly_expense = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    # Category totals

    category_totals = expenses.values(
        "category"
    ).annotate(
        total=Sum("amount")
    ).order_by(
        "-total"
    )

    # Budget

    budget = MonthlyBudget.objects.filter(
        user=request.user,
        month=month,
        year=year
    ).first()

    monthly_budget = budget.amount if budget else 0

    remaining_budget = (
        monthly_budget - monthly_expense
    )

    categories = [
        "Food",
        "Transport",
        "Study",
        "Shopping",
        "Entertainment",
        "Other"
    ]

    context = {

        "expenses": expenses,

        "monthly_expense": monthly_expense,

        "category_totals": category_totals,

        "monthly_budget": monthly_budget,

        "remaining_budget": remaining_budget,

        "categories": categories,

        "today": today,

        "month": month,

        "year": year,
    }

    return render(
        request,
        "expenses.html",
        context
    )