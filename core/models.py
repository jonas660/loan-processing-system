from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Bicycle(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class LoanApplication(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()
    
    loan_purpose = models.TextField()
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    date_applied = models.DateTimeField(default=timezone.now)

    def total_paid(self):
        return sum(payment.amount_paid for payment in self.payments.all())

    def remaining_balance(self):
        return self.loan_amount - self.total_paid()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Payment(models.Model):
    loan = models.ForeignKey(
        LoanApplication,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.loan.first_name} {self.loan.last_name} - {self.amount_paid}"

