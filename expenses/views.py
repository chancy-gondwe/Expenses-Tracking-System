from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expenses
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
import json
import datetime
import csv
import os
from django.contrib.auth.models import User
import xlwt
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum




# Create your views here.





@csrf_exempt
def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses = Expenses.objects.filter(amount__startswith=search_str, owner=request.user) | \
                   Expenses.objects.filter(date__startswith=search_str, owner=request.user) | \
                   Expenses.objects.filter(description__icontains=search_str, owner=request.user) | \
                   Expenses.objects.filter(category__icontains=search_str, owner=request.user)

        data = expenses.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='/authenticatio/login')
def index(request):
    user_prefs, created = UserPreferences.objects.get_or_create(user=request.user)
    categories = Category.objects.all()
    expenses = Expenses.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency =  UserPreferences.objects.get(user=request.user).currency
    context={
        "expenses": expenses,
        "page_obj": page_obj,
        "currency": currency,
    }
    return render(request,'expenses/index.html', context )
 

def add_expense(request):
    categories = Category.objects.all()
    # Prepare an empty values dict for GET; for POST, we'll set it below
    values = {}

    if request.method == 'POST':
        # Capture POST data for repopulating the form if needed
        values = request.POST

        # Safely get each field
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        date = request.POST.get('date')
        category = request.POST.get('category')

        # Validate each field in turn, returning early on error
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', {
                'categories': categories,
                'values': values
            })

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', {
                'categories': categories,
                'values': values
            })

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expense.html', {
                'categories': categories,
                'values': values
            })

        if not category:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/add_expense.html', {
                'categories': categories,
                'values': values
            })

        # All fields present: save the expense
        try:
            Expenses.objects.create(
                amount=amount,
                description=description,
                date=date,
                category=category,
                owner=request.user
            )
            messages.success(request, 'Expense added successfully')
            return redirect('expenses')  # ensure this name matches your expense list URL
        except Exception as e:
            # Log or inspect e if needed; here we show a generic error
            messages.error(request, 'An error occurred when saving the expense.')
            # fall through to re-render form with values
            return render(request, 'expenses/add_expense.html', {
                'categories': categories,
                'values': values
            })

    # GET request: render empty form
    return render(request, 'expenses/add_expense.html', {
        'categories': categories,
        'values': values
    })




def expense_edit(request, id):
    #expense = Expenses.objects.get(pk=id) same as below logic
    expense = get_object_or_404(Expenses, pk=id)
    categories = Category.objects.all()

    if request.method == "GET":
        context = {
            "expense": expense,
            "values": expense,
            "categories": categories,
        }
        return render(request, 'expenses/edit-expense.html', context)

    if request.method == "POST":
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('date')

        if not amount or not description or not category or not date:
            messages.error(request, 'All fields are required.')
            context = {
                "expense": expense,
                "values": request.POST,
                "categories": categories,
            }
            return render(request, 'expenses/edit-expense.html', context)

        # Update expense
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()

        messages.success(request, 'Expense updated successfully!')
        return redirect('expenses')  # Make sure 'expenses' is a valid named URL pattern


def expense_delete(request, id):
    expense = Expenses.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense removed")
    return redirect('expenses')

def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30 * 6)
    
    expenses = Expenses.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=todays_date)
    
    finalrep = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount

    for y in category_list:
        finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def stats_view(request):
    return render(request, 'expenses/stats.html')


def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    filename = f"Expenses-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expenses .objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response


def export_excel(request):
    response = HttpResponse(content_type="application/ms-excel")
    filename = f"Expenses-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xls"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')

    # Header
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Category', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Data rows
    font_style = xlwt.XFStyle()
    expenses = Expenses.objects.filter(owner=request.user).values_list('amount', 'description', 'category', 'date')

    for row in expenses:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response



def export_pdf(request):
    # Fetch the actual expenses
    expenses = Expenses.objects.filter(owner=request.user)
    total = sum(exp.amount for exp in expenses)

    # Render HTML with data
    html_string = render_to_string('expenses/pdf_output.html', {
        'expenses': expenses,
        'total': total,
    })
    html = HTML(string=html_string)

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        temp_pdf_path = temp_pdf.name

    try:
        html.write_pdf(target=temp_pdf_path)

        with open(temp_pdf_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()

        response = HttpResponse(pdf_content, content_type='application/pdf')
        filename = f"Expenses-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
        response['Content-Disposition'] = f'inline:  attachment; filename="{filename}"'
        return response

    finally:
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)