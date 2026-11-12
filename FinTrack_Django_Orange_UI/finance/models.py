from django.conf import settings
from django.db import models

class Transaction(models.Model):
    INCOME = "income"
    EXPENSE = "expense"
    TYPE_CHOICES = [(INCOME, "Income"), (EXPENSE, "Expense")]
    CATEGORY_CHOICES = [
        ("Food", "Food"),
        ("Transport", "Transport"),
        ("Entertainment", "Entertainment"),
        ("Health", "Health"),
        ("Shopping", "Shopping"),
        ("Coffee", "Coffee"),
        ("Pet", "Pet"),
        ("Gifts", "Gifts"),
        ("Rent & Bills", "Rent & Bills"),
        ("Subscriptions", "Subscriptions"),
        ("Salary", "Salary"),
        ("Other", "Other"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    title = models.CharField(max_length=70)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.type})"


class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets")
    category = models.CharField(max_length=30, choices=Transaction.CATEGORY_CHOICES)
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.DateField(help_text="Use the first day of the month.")

    class Meta:
        ordering = ["category"]
        unique_together = ("user", "category", "month")

    def __str__(self):
        return f"{self.category} — {self.month:%Y-%m}"


class DailyRate(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=30)
    rate = models.DecimalField(max_digits=20, decimal_places=6)
    unit = models.CharField(max_length=20)
    fetched_on = models.DateField()
    source = models.CharField(max_length=100, default="Official / public exchange-rate API")

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code}: {self.rate} ({self.fetched_on})"
