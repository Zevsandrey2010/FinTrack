from calendar import monthrange
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import RegisterForm, TransactionForm, BudgetForm
from .models import Transaction, Budget, DailyRate
from .rates import refresh_daily_rates

def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your personal account has been created.")
        return redirect("dashboard")
    return render(request, "finance/register.html", {"form": form})

@login_required
def dashboard(request):
    try:
        refresh_daily_rates()
    except Exception:
        pass

    today = timezone.localdate()
    month_start = today.replace(day=1)
    month_transactions = Transaction.objects.filter(user=request.user, date__year=today.year, date__month=today.month)
    all_transactions = Transaction.objects.filter(user=request.user)
    income = sum(
        (item.amount for item in month_transactions.filter(type="income")), Decimal("0.00")
    )
    expenses = sum(
        (item.amount for item in month_transactions.filter(type="expense")), Decimal("0.00")
    )
    budgets = Budget.objects.filter(user=request.user, month=month_start)
    budget_rows = []
    for budget in budgets:
        spent = sum(
            (item.amount for item in month_transactions.filter(type="expense", category=budget.category)),
            Decimal("0.00")
        )
        budget_rows.append({
            "id": budget.id,
            "category": budget.category,
            "limit": budget.limit_amount,
            "spent": spent,
            "percent": min(100, int(spent / budget.limit_amount * 100)) if budget.limit_amount else 0,
        })
    name = request.user.first_name or request.user.username
    category_totals = []
    for category, _label in Transaction.CATEGORY_CHOICES:
        total = sum(
            (item.amount for item in month_transactions.filter(type="expense", category=category)),
            Decimal("0.00")
        )
        if total > 0:
            category_totals.append({"category": category, "total": total})
    return render(request, "finance/dashboard.html", {
        "transactions": all_transactions[:100],
        "income": income,
        "expenses": expenses,
        "balance": income - expenses,
        "savings_percent": max(0, round((income - expenses) / income * 100)) if income else 0,
        "budgets": budget_rows,
        "rates": DailyRate.objects.all(),
        "rates_updated": DailyRate.objects.order_by("-fetched_on").values_list("fetched_on", flat=True).first(),
        "display_name": name,
        "current_month": month_start,
        "category_choices": Transaction.CATEGORY_CHOICES,
        "category_totals": category_totals,
    })

@login_required
@require_POST
def transaction_create(request):
    form = TransactionForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        messages.success(request, "Transaction added successfully.")
    else:
        messages.error(request, "Please check the transaction details and try again.")
    return redirect("dashboard")

@login_required
@require_POST
def transaction_delete(request, pk):
    item = get_object_or_404(Transaction, pk=pk, user=request.user)
    item.delete()
    messages.success(request, "Transaction deleted.")
    return redirect("dashboard")

@login_required
def budget_create(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.month = item.month.replace(day=1)
            item.save()
            messages.success(request, "Budget saved.")
            return redirect("dashboard")
    else:
        form = BudgetForm(initial={"month": timezone.localdate().replace(day=1)})
    return render(request, "finance/budget_form.html", {"form": form})

@login_required
@require_POST
def budget_delete(request, pk):
    item = get_object_or_404(Budget, pk=pk, user=request.user)
    item.delete()
    messages.success(request, "Budget deleted.")
    return redirect("dashboard")

@login_required
def profile_view(request):
    return render(request, "finance/profile.html", {"display_name": request.user.first_name or request.user.username})

@login_required
def reports_view(request):
    transactions = Transaction.objects.filter(user=request.user)
    total_income = sum((t.amount for t in transactions.filter(type="income")), Decimal("0.00"))
    total_expenses = sum((t.amount for t in transactions.filter(type="expense")), Decimal("0.00"))
    return render(request, "finance/reports.html", {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_total": total_income - total_expenses,
        "transaction_count": transactions.count(),
    })
