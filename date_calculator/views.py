from django.shortcuts import render

def index(request):
    return render(
        request,
        'date_calculator/index.html',
    )
