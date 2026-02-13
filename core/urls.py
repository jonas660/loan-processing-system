from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('apply-loan/', views.loan_application, name='loan_application'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('staff-list/', views.staff_list, name='staff_list'),
    path('inventory/', views.inventory_bike, name='inventory_bike'),
    path('loans/', views.loans, name='loans'),
    path('approved-loans/', views.approved_loans, name='approved_loans'),
    path('add-payment/<int:loan_id>/', views.add_payment, name='add_payment'),
]
