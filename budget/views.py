# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import ExtractMonth  # pro extrakci měsíce
from .forms import RegistrationForm, TransactionForm
from .models import Transaction, Note  # Ujistěte se, že máte definované modely
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
        return redirect('dashboard')
    return render(request, 'budget/confirm_delete_note.html', {'note': note})

@csrf_exempt  # Pro vývoj – v produkci používejte CSRF token správně.
def save_note(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            note_content = data.get('note', '')
            if note_content:
                Note.objects.create(content=note_content)
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'Empty note'})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False}, status=400)

def contact(request):
    return render(request, 'budget/contact.html')

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        transaction.delete()
        return redirect('transaction_list')
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
    # Načtení transakcí přihlášeného uživatele
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    total_income = transactions.filter(category__type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(category__type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    # Agregace transakcí podle měsíce – získáme součet za každý měsíc
    monthly_data_query = (
        Transaction.objects.filter(user=request.user)
        .annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    # Inicializujeme seznam pro 12 měsíců (index 0 = leden, index 11 = prosinec)
    monthly_totals = [0] * 12
    for record in monthly_data_query:
        month_index = record['month'] - 1
        monthly_totals[month_index] = record['total'] or 0

    # Názvy měsíců
    month_labels = [
        "Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
        "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"
    ]

    # Načtení uložených poznámek – nejnovější jako první
    saved_notes = Note.objects.all().order_by('-created_at')

    context = {
        'transactions': transactions[:5],  # Zobrazíme 5 nejnovějších transakcí
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'monthly_labels': month_labels,     # Seznam názvů měsíců
        'monthly_data': monthly_totals,       # Seznam součtů transakcí za měsíce
        'saved_notes': saved_notes,
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

    total_income = transactions.filter(category__type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(category__type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'period': period,
    }
    return render(request, 'budget/transaction_list.html', context)

def privacy_policy(request):
    return render(request, 'budget/privacy_policy.html')
