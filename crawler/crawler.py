# -*- coding: utf-8 -*-

from gevent import spawn, sleep
from gevent.queue import Queue
import requests
import ujson


requests.packages.urllib3.disable_warnings()


class BaseCrawler():
    url = ''
    name = ''
    page_limit = 100
    limit = 200

    @classmethod
    def crawl(cls):
        car_queue = Queue(cls.limit)

        def worker():
            page = 0
            count = 0
            while count < cls.limit:
                sleep(1)
                result = requests.post(cls.url, data=cls._get_request_data(page, cls.page_limit))
                print result.status_code, '|||', cls.url
                cars = cls._get_cars(result)
                for car in cars:
                    car_queue.put(car)
                    count += 1
                    if count >= cls.limit:
                        car_queue.put(None)
                        return
                if len(cars) < cls.page_limit:
                    break
                page += 1
            car_queue.put(None)

        spawn(worker)

        for car in car_queue:
            if car is None:
                return
            try:
                yield cls._parse_car(car)
            except:
                print car
                raise

    @classmethod
    def _get_cars(cls, result):
        raise NotImplementedError()

    @classmethod
    def _parse_car(cls, raw):
        raise NotImplementedError()

    @classmethod
    def _get_request_data(cls, page, page_limit):
        raise NotImplementedError()


class VroomCrawler(BaseCrawler):
    url = 'https://www.vroom.com/catalog'
    url_by_type = 'https://www.vroom.com/catalog/all-years/all-makes/{type}?sort=year'
    name = 'vroom'
    page_limit = 50
    limit = 400

    TYPES = {
        'convertible' : 'convertible',
        'coupe': 'coupe',
        'hatchback': 'hatchback',
        'mini-van': 'minivan',
        'sedan': 'sedan',
        'suv': 'suv',
        'truck': 'truck',
        'wagon': 'wagon',
    }

    @classmethod
    def crawl(cls):
        car_queue = Queue(cls.limit)

        def worker():
            for url_type, body_type in cls.TYPES.iteritems():
                url = cls.url_by_type.format(type=url_type)
                page = 0
                sleep(1)
                result = requests.post(url, data=cls._get_request_data(page, cls.page_limit))
                print result.status_code, '|||', cls.url
                cars = cls._get_cars(result)
                for car in cars:
                    car['body_type'] = body_type
                    car_queue.put(car)
            car_queue.put(None)

        spawn(worker)

        for car in car_queue:
            if car is None:
                return
            try:
                yield cls._parse_car(car)
            except:
                print car
                raise

    @classmethod
    def _get_cars(cls, result):
        return ujson.loads(result.text)['Data']['Cars']['CarsList']

    @classmethod
    def _parse_car(cls, raw):
        return dict(
            make=raw['Make'],
            model=raw['Model'],
            trim=raw['Trim'],
            price=float(raw['Price']),
            year=int(raw['Year']),
            mileage=int(raw['Mileage']),
            product_url='https://www.vroom.com' + raw['Url'],
            image_url=raw['Image'],
            product_id=raw['Id'],
            platform_name=cls.name,
            body_type=raw['body_type'],
        )

    @classmethod
    def _get_request_data(cls, page, page_limit):
        return dict(PageSize=page_limit, SkipVehiclesAmount=page * page_limit)


class BeepiCrawler(BaseCrawler):
    url = 'https://www.beepi.com/v1/listings/carsPageResults'
    name = 'beepi'
    page_limit = 21

    TYPES = {
        'convertible' : 'convertible',
        'coupe': 'coupe',
        'hatchback': 'hatchback',
        'minivan': 'minivan',
        'sedan': 'sedan',
        'suv': 'suv',
        'pick up': 'truck',
        'wagon': 'wagon',
    }

    @classmethod
    def _get_cars(cls, result):
        return ujson.loads(result.text)['carsOnSale']

    @classmethod
    def _parse_car(cls, raw):
        return dict(
            make=raw['makeName'],
            model=raw['modelName'],
            trim=raw['trim'],
            price=float(raw['salePrice']),
            year=int(raw['year']),
            mileage=int(raw['mileage']),
            product_url='https://www.beepi.com' + raw['carPageUrl'],
            image_url='http:' + raw['carShotUrls']['heroShotUrl'],
            product_id=raw['vin'],
            platform_name=cls.name,
            body_type=cls.TYPES.get(raw['bodyType'].lower(), 'other')
        )

    @classmethod
    def _get_request_data(cls, page, page_limit):
        return dict(searchQueryId=6, pageId=page)
