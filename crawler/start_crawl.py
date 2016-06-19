import sys
sys.path.append('./')
from lib.config import create_app
create_app('prod')

from django.core.exceptions import ObjectDoesNotExist
from gevent import spawn
from gevent.queue import Queue

from carsapp.models import Car
from crawler import VroomCrawler, BeepiCrawler


CRAWLERS = [VroomCrawler, BeepiCrawler]


def run():
    car_queue = Queue()
    crawler_finished = 0

    def worker(crawler):
        for datum in crawler.crawl():
            car_queue.put(datum)
        car_queue.put(None)

    for crawler in CRAWLERS:
        spawn(worker, crawler)

    for datum in car_queue:
        if datum is None:
            crawler_finished += 1
            if crawler_finished >= len(CRAWLERS):
                return
            else:
                continue
        try:
            car = Car.objects.get(product_id=datum['product_id'], platform_name=datum['platform_name'])
            car.update_with(**datum)
        except ObjectDoesNotExist:
            Car.save_with(**datum)


if __name__ == "__main__":
    run()
