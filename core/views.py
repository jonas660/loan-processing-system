from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from core.models import LoanApplication
from .forms import StaffCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Bicycle, LoanApplication


def inventory_bike(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add":
            Bicycle.objects.create(
                name=request.POST["name"],
                quantity=int(request.POST["quantity"]),
                price=float(request.POST["price"])
            )
            messages.success(request, "Bicycle added successfully.")

        elif action == "edit":
            bicycle = get_object_or_404(Bicycle, id=request.POST["bicycle_id"])
            bicycle.quantity = int(request.POST["quantity"])
            bicycle.price = float(request.POST["price"])
            bicycle.save()
            messages.success(request, "Bicycle updated successfully.")

        elif action == "delete":
            bicycle = get_object_or_404(Bicycle, id=request.POST["bicycle_id"])
            bicycle.delete()
            messages.success(request, "Bicycle deleted successfully.")

        return redirect("inventory_bike")

    inventory = Bicycle.objects.all()
    return render(request, "inventory_bike.html", {"inventory": inventory})
        
def admin_only(user):
    return user.is_superuser

@login_required
@user_passes_test(admin_only)
def add_staff(request):
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_list')
    else:
        form = StaffCreationForm()

    return render(request, 'add_staff.html', {'form': form})

@login_required
@user_passes_test(admin_only)
def staff_list(request):
    staffs = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'staff_list.html', {'staffs': staffs})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def landing(request):
    return render(request, 'landing.html')

# Create your views hereration

@login_required
def loan_application(request):
    bicycles = Bicycle.objects.filter(quantity__gt=0)

    if request.method == "POST":
        bike_id = request.POST.get("bicycle")
        term = request.POST.get("term")
        message = request.POST.get("message")

        bike = get_object_or_404(Bicycle, id=bike_id)

        LoanApplication.objects.create(
            user=request.user,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            address="N/A",  # change if you collect address
            contact_number="N/A",  # change if needed
            loan_amount=bike.price,
            loan_purpose=message,
            proof_of_income="proof_of_income/default.pdf",  # temporary
            valid_id="valid_ids/default.pdf"  # temporary
        )
        bicycle.quantity -= 1
        bicycle.save()

        messages.success(request, "Loan application submitted successfully!")
        return redirect("dashboard")

    return render(request, 'loan_application.html', {'bicycles': bicycles})


@login_required
def loans(request):
    loans = LoanApplication.objects.all().order_by('-date_applied')
    return render(request, 'loans.html', {'loans': loans})

def approved_loans(request):
    loans = LoanApplication.objects.filter(status='APPROVED')
    return render(request, 'approved_loans.html', {'loans': loans})


def add_payment(request, loan_id):
    loan = get_object_or_404(LoanApplication, id=loan_id)

    if request.method == "POST":
        amount = request.POST.get('amount')

        Payment.objects.create(
            loan=loan,
            amount_paid=amount
        )

        messages.success(request, "Payment recorded successfully.")
        return redirect('approved_loans')

    return render(request, 'add_payment.html', {'loan': loan})

def loan_soa(request, loan_id):
    loan = LoanApplication.objects.get(id=loan_id)

    principal = loan.bicycle.price
    term = loan.term  # "3 months", "6 months", "9 months"

    # Set interest rate
    if term == "3 months":
        months = 3
        interest_rate = 0.0368
    elif term == "6 months":
        months = 6
        interest_rate = 0.0425
    elif term == "9 months":
        months = 9
        interest_rate = 0.06
    else:
        months = 1
        interest_rate = 0

    # Compute interest
    total_interest = principal * interest_rate
    total_payable = principal + total_interest
    monthly_payment = total_payable / months

    context = {
        "loan": loan,
        "principal": principal,
        "months": months,
        "interest_rate": interest_rate * 100,
        "total_interest": total_interest,
        "total_payable": total_payable,
        "monthly_payment": monthly_payment,
    }

    return render(request, "loan_soa.html", context)

