from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, UserIncome
from django.core.paginator import Paginator
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import UserIncome, Source
import json
from django.http import JsonResponse
import datetime
from django.shortcuts import render
from .models import UserIncome

from userpreferences.models import UserPreferences



# Create your views here.

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText', '')

        incomes = UserIncome.objects.filter(owner=request.user).filter(
            amount__startswith=search_str
        ) | UserIncome.objects.filter(owner=request.user).filter(
            date__startswith=search_str
        ) | UserIncome.objects.filter(owner=request.user).filter(
            description__icontains=search_str
        ) | UserIncome.objects.filter(owner=request.user).filter(
            source__name__icontains=search_str
        )

        data = incomes.values('id', 'amount', 'date', 'description', 'source__name')

        results = []
        for item in data:
            item['source'] = item.pop('source__name', '')
            results.append(item)

        return JsonResponse(results, safe=False)

@login_required(login_url='/authenticatio/login')
def index(request):
    categories = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency =  UserPreferences.objects.get(user=request.user).currency
    context={
        "income": income,
        "page_obj": page_obj,
        "currency": currency,
    }
    return render(request,'income/index.html', context )
 


def add_income(request):
    sources = Source.objects.all()
    values = {}

    if request.method == 'POST':
        values = request.POST
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        source_id = request.POST.get('source')

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', {'sources': sources, 'values': values})

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', {'sources': sources, 'values': values})

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/add_income.html', {'sources': sources, 'values': values})

        if not source_id:
            messages.error(request, 'Source is required')
            return render(request, 'income/add_income.html', {'sources': sources, 'values': values})

        try:
            amount = Decimal(amount)
            source_instance = Source.objects.get(id=source_id)

            UserIncome.objects.create(
                amount=amount,
                description=description,
                date=date,
                source=source_instance,
                owner=request.user
            )
            messages.success(request, 'Income added successfully')
            return redirect('income')

        except InvalidOperation:
            messages.error(request, 'Enter a valid number for amount')
        except Source.DoesNotExist:
            messages.error(request, 'Selected source does not exist')
        except Exception as e:
            print("DEBUG ERROR:", e)  # Add this to see the actual issue in terminal
            messages.error(request, 'An error occurred when saving the income.')

        return render(request, 'income/add_income.html', {'sources': sources, 'values': values})

    # GET request
    return render(request, 'income/add_income.html', {'sources': sources, 'values': values})




def income_edit(request, id):
    income = get_object_or_404(UserIncome, pk=id, owner=request.user)
    sources = Source.objects.all()
    values = request.POST if request.method == 'POST' else {
        'amount': income.amount,
        'description': income.description,
        'date': income.date,
        'source': income.source
    }

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        source_id = request.POST.get('source')

        if not all([amount, description, date, source_id]):
            messages.error(request, 'All fields are required.')
            return render(request, 'income/edit_income.html', {
                'income': income,
                'sources': sources,
                'values': values
            })

        try:
            income.amount = Decimal(amount)
            income.description = description
            income.date = date
            income.source = Source.objects.get(id=source_id)
            income.save()
            messages.success(request, 'Income updated successfully')
            return redirect('income')
        except (InvalidOperation, Source.DoesNotExist):
            messages.error(request, 'Invalid input. Please check your data.')
    
    return render(request, 'income/edit_income.html', {
        'income': income,
        'sources': sources,
        'values': values
    })

def income_delete(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, "Income removed")
    return redirect('income')

def income_category_summary(request):
    today = datetime.date.today()
    six_months_ago = today - datetime.timedelta(days=30 * 6)

    incomes = UserIncome.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=today)

    final_report = {}

    for income in incomes:
        source = income.source.name if income.source else "Unknown"
        if source in final_report:
            final_report[source] += income.amount
        else:
            final_report[source] = income.amount

    return JsonResponse({'income_category_data': final_report}, safe=False)

def income_stats_view(request):
    return render(request, 'income/stats.html')
