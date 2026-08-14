from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):

    CATEGORY_CHOICES = [
        ("Food", "Food"),
        ("Transport", "Transport"),
        ("Study", "Study"),
        ("Shopping", "Shopping"),
        ("Entertainment", "Entertainment"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField(
        blank=True
    )

    date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.category} - {self.amount}"



class MonthlyBudget(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    month = models.PositiveIntegerField()

    year = models.PositiveIntegerField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "month", "year"],
                name="unique_user_monthly_budget"
            )
        ]


    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}"