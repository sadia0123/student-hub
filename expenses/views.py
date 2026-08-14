from django.shortcuts import render


# Create your views here.
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Expense, MonthlyBudget
from .serializers import ExpenseSerializer, MonthlyBudgetSerializer


class ExpenseListView(ListCreateAPIView):

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(
            user=self.request.user
        ).order_by("-date", "-created_at")

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class ExpenseDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(
            user=self.request.user
        )
    
from django.db.models import Sum
from rest_framework.response import Response    
class ExpenseSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        expenses = Expense.objects.filter(
            user=request.user
        )

        total = expenses.aggregate(
            total=Sum("amount")
        )["total"] or 0

        food = expenses.filter(
            category="Food"
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        transport = expenses.filter(
            category="Transport"
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        study = expenses.filter(
            category="Study"
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        shopping = expenses.filter(
            category="Shopping"
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        entertainment = expenses.filter(
            category="Entertainment"
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        other = expenses.filter(
            category="Other"
        ).aggregate(
            total=Sum("amount")
        )["total"] or 0

        return Response({
            "total": total,
            "food": food,
            "transport": transport,
            "study": study,
            "shopping": shopping,
            "entertainment": entertainment,
            "other": other
        })
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class MonthlyExpenseSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        month = request.query_params.get("month")
        year = request.query_params.get("year")

        expenses = Expense.objects.filter(
            user=request.user
        )

        if month and year:

            expenses = expenses.filter(
                date__month=month,
                date__year=year
            )

        total = expenses.aggregate(
            total=Sum("amount")
        )["total"] or 0

        return Response({
            "month": month,
            "year": year,
            "total": total
        })    

class MonthlyBudgetListView(ListCreateAPIView):

    serializer_class = MonthlyBudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MonthlyBudget.objects.filter(
            user=self.request.user
        ).order_by("-year", "-month")

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )   




from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response


class BudgetSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        month = request.query_params.get("month")
        year = request.query_params.get("year")

        if not month or not year:
            return Response({
                "error": "month and year are required."
            })

        budget = MonthlyBudget.objects.filter(
            user=request.user,
            month=month,
            year=year
        ).first()

        if not budget:
            return Response({
                "error": "No budget found for this month."
            })

        expenses = Expense.objects.filter(
            user=request.user,
            date__month=month,
            date__year=year
        )

        spent = expenses.aggregate(
            total=Sum("amount")
        )["total"] or 0

        remaining = budget.amount - spent

        return Response({
            "month": month,
            "year": year,
            "budget": budget.amount,
            "spent": spent,
            "remaining": remaining
        })