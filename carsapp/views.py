from django.shortcuts import render

from carsapp.models import Car


def index(request):
    params = _parse_request(request)
    page = (int(params['page']) - 1) if params['page'] else 0
    limit = int(params['limit']) if params['limit'] else 21
    start = page * limit
    end = start + limit

    cars = Car.objects.all()
    if params['make']:
        cars = cars.filter(make=params['make'])
        print params['make'], cars.count()
    if params['body_type']:
        cars = cars.filter(body_type=params['body_type'])
    if params['year_min']:
        cars = cars.filter(year__gte=int(params['year_min']))
    if params['year_max']:
        cars = cars.filter(year__lte=int(params['year_max']))
    if params['price_min']:
        cars = cars.filter(price__gte=int(params['price_min']))
    if params['price_max']:
        cars = cars.filter(price__lte=int(params['price_max']))
    if params['mileage_min']:
        cars = cars.filter(mileage__gte=int(params['mileage_min']))
    if params['mileage_max']:
        cars = cars.filter(mileage__lte=int(params['mileage_max']))
    
    context = dict(
        cars=cars[start:end],
        body_types=Car.TYPES,
        makes=Car.MAKES,
        params=params)

    return render(request, 'carsapp/index.html', context)


def _parse_request(request):
    params = {}
    params['page'] = request.GET.get('page', '')
    if not params['page']:
        params['page'] = 1
    params['limit'] = request.GET.get('limit', '')
    params['year_min'] = request.GET.get('year_min', '')
    params['year_max'] = request.GET.get('year_max', '')
    params['price_min'] = request.GET.get('price_min', '')
    params['price_max'] = request.GET.get('price_max', '')
    params['mileage_min'] = request.GET.get('mileage_min', '')
    params['mileage_max'] = request.GET.get('mileage_max', '')
    params['body_type'] = request.GET.get('body_type', '')
    params['make'] = request.GET.get('make', '')
    return params
