from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
class Expense(models.Model):
    category_choices=[
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Entertainment', 'Entertainment'),
        ('Shopping', 'Shopping'),
        ('Rent', 'Rent'),
        ('salary','salary'),
        ('Other', 'Other'),
    ]
    TYPE_CHOICES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.CharField(max_length=100,choices=category_choices)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - ₹{self.amount} ({self.type})"