from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from finance import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="finance/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("transactions/add/", views.transaction_create, name="transaction_create"),
    path("transactions/<int:pk>/delete/", views.transaction_delete, name="transaction_delete"),
    path("budgets/add/", views.budget_create, name="budget_create"),
    path("budgets/<int:pk>/delete/", views.budget_delete, name="budget_delete"),
    path("profile/", views.profile_view, name="profile"),
    path("reports/", views.reports_view, name="reports"),
]
