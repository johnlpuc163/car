# -*- coding: utf-8 -*-

from gevent import spawn
from gevent.queue import Queue
import requests
import ujson


class BaseCrawler():
    url = ''
    name = ''
    page_limit = 100

    @classmethod
    def crawl(cls, limit=200):
        car_queue = Queue(limit)

        def worker():
            page = 0
            count = 0
            while count < limit:
                result = requests.post(cls.url, data=cls._get_request_data(page, cls.page_limit))
                print result.status_code, '|||', cls.url
                cars = cls._get_cars(result)
                for car in cars:
                    car_queue.put(car)
                    count += 1
                    if count >= limit:
                        car_queue.put(None)
                        return
                if len(cars) < cls.page_limit:
                    break
                page += 1
            cars.put(None)

        spawn(worker)

        for car in car_queue:
            if car is None:
                return
            yield cls._parse_car(car)

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
    name = 'vroom'

    @classmethod
    def _get_cars(cls, result):
        return ujson.loads(result.text)['Data']['Cars']

    @classmethod
    def _parse_car(cls, raw):
        return dict(
            make=raw['Make'],
            model=raw['Model'],
            trim=raw['Trim'],
            price=float(raw['Price']),
            year=int(raw['Year']),
            mileage=int(raw['Mileage']),
            product_url='https://www.vroom.com' + raw['ProductUrl'],
            image_url=raw['Images'][0],
            product_id=raw['Id'],
            platform_name=cls.name
        )

    @classmethod
    def _get_request_data(cls, page, page_limit):
        return dict(PageSize=page_limit, SkipVehiclesAmount=page * page_limit)


class BeepiCrawler(BaseCrawler):
    url = 'https://www.beepi.com/v1/listings/carsPageResults'
    name = 'beepi'
    page_limit = 21

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
            platform_name=cls.name
        )

    @classmethod
    def _get_request_data(cls, page, page_limit):
        return dict(searchQueryId=6, pageId=page)
