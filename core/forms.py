from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import LoanApplication
from .models import Payment


class StaffCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True     # staff user
        user.is_active = True
        if commit:
            user.save()
        return user

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Gmail address'
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username.endswith('@gmail.com'):
            raise ValidationError("Username must be a Gmail address (@gmail.com)")

        if User.objects.filter(username=username).exists():
            raise ValidationError("This email is already registered")

        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # hash password
        if commit:
            user.save()
        return user

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = [
            'first_name',
            'last_name',
            'contact_number',
            'address',
            'loan_purpose',
            'loan_amount',
            'proof_of_income',
            'valid_id'
        ]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount_paid']