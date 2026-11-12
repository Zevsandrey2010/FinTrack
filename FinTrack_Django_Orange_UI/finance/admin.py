from django.contrib import admin
from .models import Transaction, Budget, DailyRate

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "type", "category", "amount", "date")
    list_filter = ("type", "category", "date")
    search_fields = ("title", "user__username", "user__email")

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("category", "user", "limit_amount", "month")
    list_filter = ("category", "month")
    search_fields = ("user__username",)

@admin.register(DailyRate)
class DailyRateAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "rate", "unit", "fetched_on", "source")
    readonly_fields = ("code", "name", "rate", "unit", "fetched_on", "source")
