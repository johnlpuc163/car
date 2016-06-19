from django.shortcuts import render

from carsapp.models import Car


def index(request):
    page = int(request.GET.get('page', 0))
    limit = int(request.GET.get('limit', 20))
    start = page * limit
    end = start + limit
    context = dict(cars=Car.objects.all()[start:end])
    return render(request, 'carsapp/index.html', context)
