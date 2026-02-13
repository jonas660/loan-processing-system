from django.contrib import admin
from .models import LoanApplication, Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'loan_amount', 'status', 'remaining_balance')
    inlines = [PaymentInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'amount_paid', 'payment_date')
