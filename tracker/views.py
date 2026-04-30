from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum
from .models import Expense


# 🏠 Home (optional)
def home(request):
    return HttpResponse("🏠 Home Page Working!")


# ➕ Add Expense
@login_required
def add_expense(request):
    if request.method == "POST":
        desc = request.POST.get('description')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        date = request.POST.get('date')

        Expense.objects.create(
            user=request.user,
            description=desc,
            amount=amount,
            category=category,
            date=date
        )

        return redirect('/add/')

    return render(request, 'add_expense.html')


# 📊 Dashboard (FIXED VERSION ✅)
@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)

    # ✅ TOTAL AMOUNT
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    # ✅ CATEGORY CHART
    category_data = expenses.values('category').annotate(total=Sum('amount'))

    labels = [item['category'] for item in category_data]
    data = [float(item['total']) for item in category_data]

    return render(request, 'dashboard.html', {
        'expenses': expenses,
        'labels': labels,
        'data': data,
        'total': total   # 🔥 IMPORTANT
    })


# ❌ Delete Expense
@login_required
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    return redirect('/')


# ✏️ Edit Expense
@login_required
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        expense.description = request.POST.get('description')
        expense.amount = request.POST.get('amount')
        expense.category = request.POST.get('category')
        expense.date = request.POST.get('date')
        expense.save()
        return redirect('/')

    return render(request, 'edit_expense.html', {'expense': expense})