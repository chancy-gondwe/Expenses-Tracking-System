from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from .models import UserPreferences
import os
import json

def index(request):
    exists = UserPreferences.objects.filter(user=request.user).exists()
    user_preferences = None

    if exists:
        user_preferences = UserPreferences.objects.get(user=request.user)

    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    if request.method == "GET":
        return render(request, 'preferences/index.html', {
            'currencies': currency_data,
            'selected_currency': user_preferences.currency if user_preferences else None
        })

    else:  # POST
        currency = request.POST.get('currency')

        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            UserPreferences.objects.create(user=request.user, currency=currency)

        messages.success(request, 'Changes saved')
        return render(request, 'preferences/index.html', {
            'currencies': currency_data,
            'selected_currency': currency
        })
