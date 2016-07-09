from django.shortcuts import render

from carsapp.models import Car


def index(request):
    # page = request.GET.get('page', None)
    # page = int(page) if page else 0
    # limit = request.GET.get('limit', None)
    # limit = int(limit) if limit else 20
    params = _parse_request(request)
    page = (int(params['page']) - 1) if params['page'] else 0
    limit = int(params['limit']) if params['limit'] else 20
    start = page * limit
    end = start + limit

    year_min = int(params['year_min']) if params['year_min'] else None
    makes = {'benz', 'audi', 'bmw'}
    context = dict(
        cars=Car.objects.all()[start:end],
        body_types=Car.TYPES,
        makes=makes,
        params=params)
    return render(request, 'carsapp/index.html', context)


def _parse_request(request):
    params = {}
    params['page'] = request.GET.get('page', '')
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
