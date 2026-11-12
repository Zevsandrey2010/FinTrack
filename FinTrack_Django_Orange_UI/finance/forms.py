from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction, Budget

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, initial="Андрей Кочкарь", label="Full name")
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "full_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["full_name"].strip()
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("title", "type", "category", "amount", "date")
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ("category", "limit_amount", "month")
        widgets = {"month": forms.DateInput(attrs={"type": "date"})}
