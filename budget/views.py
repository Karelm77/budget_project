from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .forms import RegistrationForm, TransactionForm
from .models import Transaction

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        transaction.delete()
        return redirect('transaction_list')  # nebo můžete přesměrovat na dashboard
    return render(request, 'budget/confirm_delete.html', {'transaction': transaction})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'budget/register.html', {'form': form})


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    total_income = transactions.filter(category__type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(category__type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense
    context = {
        'transactions': transactions[:5],  # zobrazení pěti nejnovějších transakcí
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
    }
    return render(request, 'budget/dashboard.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'budget/add_transaction.html', {'form': form})


@login_required
def transaction_list(request):
    period = request.GET.get('period')
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    now = timezone.now().date()

    if period == 'week':
        start_week = now - timedelta(days=now.weekday())
        transactions = transactions.filter(date__gte=start_week)
    elif period == 'month':
        transactions = transactions.filter(date__year=now.year, date__month=now.month)

    total_income = transactions.filter(category__type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(category__type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'period': period
    }
    return render(request, 'budget/transaction_list.html', context)



