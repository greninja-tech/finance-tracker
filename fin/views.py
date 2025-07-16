from django.shortcuts import render
from fin.forms import Register,Login,ExpenseForm
from fin.models import User,Expense
from django.contrib import messages
from django.shortcuts import render,redirect
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from collections import defaultdict
from django.template.loader import render_to_string
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Create your views here.

def register(request):
    if request.method == "POST":
        form = Register(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']
            income = form.cleaned_data['income']

            user = User(name=name, email=email, income=income,password=password)
            user.save()
            messages.success(request, "Account created successfully")
            return redirect('login')
        else:
            return render(request, 'fin/register.html', {'form': form})
    else:
        form = Register()
        return render(request, 'fin/register.html', {'form': form})


    
def login_view(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.password==password:
                    request.session['user_id']=user.id
                    messages.success(request, f"Welcome back, {user.name}")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Invalid email or password")
            except:
                messages.error(request, "Invalid email or password")
    else:
        form = Login()
    return render(request, 'fin/login.html', {'form': form})

def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            user_id = request.session.get('user_id')
            if not user_id:
                messages.error(request, "User session expired. Please login again.")
                return redirect('login')
            expense.user = User.objects.get(id=user_id)
            expense.save()
            messages.success(request, "Transaction added successfully!")
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    return render(request, 'fin/add_expense.html', {'form': form})

def view_expense(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "User session expired. Please login again.")
        return redirect('login')
    expenses=Expense.objects.filter(user_id=user_id).order_by('-date')
    return render(request,'fin/view_expense.html',{'expenses':expenses})

def analytics(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    category_data = (
        Expense.objects
        .filter(user_id=user_id, type='EXPENSE')
        .values('category')
        .annotate(total=Sum('amount'))
    )
    labels = [item['category'] for item in category_data]
    data = [float(item['total']) for item in category_data]

    monthly_data = (
        Expense.objects
        .filter(user_id=user_id)
        .annotate(month=TruncMonth('date'))
        .values('month', 'type')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    from collections import OrderedDict
    month_dict = OrderedDict()
    for entry in monthly_data:
        month_name = entry['month'].strftime('%B %Y')
        if month_name not in month_dict:
            month_dict[month_name] = {'INCOME': 0, 'EXPENSE': 0}
        month_dict[month_name][entry['type']] = float(entry['total'])

    months = list(month_dict.keys())
    income = [month_dict[m]['INCOME'] for m in months]
    expense = [month_dict[m]['EXPENSE'] for m in months]

    return render(request, 'fin/analytics.html', {
        'labels': labels,
        'data': data,
        'months': months,
        'income': income,
        'expense': expense,
    })

def dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)

    total_salary_added = Expense.objects.filter(
        user=user, category='salary', type='INCOME'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    total_expense = Expense.objects.filter(
        user=user, type='EXPENSE'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    available_balance = user.income+total_salary_added - total_expense

    last_transactions = Expense.objects.filter(
        user=user
    ).order_by('-date')[:5]

    context = {
        'user': user,
        'total_salary_added': total_salary_added,
        'total_expense': total_expense,
        'available_balance': available_balance,
        'last_transactions': last_transactions,
    }

    return render(request, 'fin/dashboard.html', context)

def download_pdf(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)
    expenses = Expense.objects.filter(user=user).order_by('-date')

    # Create HTTP response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transaction_history.pdf"'

    # Create PDF canvas
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, y, f"{user.name}'s Transaction History")
    y -= 40

    # Column Headers
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Title")
    p.drawString(150, y, "Amount")
    p.drawString(250, y, "Category")
    p.drawString(350, y, "Type")
    p.drawString(450, y, "Date")
    y -= 20

    # Content
    p.setFont("Helvetica", 10)
    for txn in expenses:
        if y < 50:
            p.showPage()
            y = height - 50
            p.setFont("Helvetica", 10)

        p.drawString(50, y, txn.title[:20])
        p.drawString(150, y, f"₹{txn.amount}")
        p.drawString(250, y, txn.category)
        p.drawString(350, y, txn.type)
        p.drawString(450, y, txn.date.strftime('%Y-%m-%d'))
        y -= 20

    p.showPage()
    p.save()
    return response

    