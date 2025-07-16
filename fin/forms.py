from django import forms
from fin.models import Expense,User
from django.core.exceptions import ValidationError

class Register(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'password','income')
        
        labels = {
            'username': 'Name',
            'email': 'Email',
            'password': 'Password',
            'income': 'Income',
        }
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'income': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your income'})
        }
        def clean_email(self):
            email = self.cleaned_data.get('email').lower()
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email already exists.")
            return email


class Login(forms.Form):
    email=forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        label="Password"
    )
    
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'type', 'date'] 

        labels = {
            'title': 'Title',
            'amount': 'Amount (₹)',
            'category': 'Category',
            'type': 'Transaction Type',
            'date': 'Date',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Rent, Bonus, Pizza'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        return amount