from django.urls import path
from .import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
        path('', views.index, name='income'),
        path('add-income/', views.add_income, name='add-income'),
        path('edit-income/<int:id>', views.income_edit, name='edit-income'),
        path('income-delete/<int:id>', views.income_delete, name='income_delete'), 
        path('search-income', views.search_income, name='search-income'),
        #path('search-income', csrf_exempt(views.search_income), name='search-income'), 
    path('income_category_summary', views.income_category_summary, name='income_category_summary'),
    path('income/stats', views.income_stats_view, name='income_stats'),



]
 