from django.urls import path

from .views import (
    ExpenseListView,
    ExpenseDetailView,
    ExpenseSummaryView,
    MonthlyExpenseSummaryView,
    MonthlyBudgetListView,
    BudgetSummaryView,
)

urlpatterns = [

    path(
        "expenses/",
        ExpenseListView.as_view()
    ),

    path(
        "expenses/<int:pk>/",
        ExpenseDetailView.as_view()
    ),
    path(
    "expenses/summary/",
    ExpenseSummaryView.as_view()
),
path(
        "expenses/<int:pk>/",
        ExpenseDetailView.as_view()
    ),
    path(
    "expenses/monthly/",
    MonthlyExpenseSummaryView.as_view()
),

path(
    "budgets/",
    MonthlyBudgetListView.as_view()
),
path(
    "budgets/summary/",
    BudgetSummaryView.as_view()
),
]