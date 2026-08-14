from rest_framework import serializers
from .models import Expense, MonthlyBudget


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id",
            "amount",
            "category",
            "description",
            "date",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class MonthlyBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBudget
        fields = [
            "id",
            "month",
            "year",
            "amount",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]               