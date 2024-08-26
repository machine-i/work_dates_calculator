from django.urls import path
from date_calculator import views

app_name = 'date_calculator'

urlpatterns = [
    path('', views.index, name='index'),
    path('calculate/', views.calculate, name='calculate'),
]
