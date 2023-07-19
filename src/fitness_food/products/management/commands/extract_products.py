from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from urllib.error import HTTPError
from urllib.request import urlopen

import sentry_sdk
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from fitness_food.products.facade import (
    get_products_url,
    get_soup_product_detail,
    update_or_create_product,
)


class Command(BaseCommand):
    help = 'Extract products from Open Food Facts website.'
    BASE_URL = 'https://world.openfoodfacts.org/'

    def handle(self, *args, **options):
        initial_time = datetime.now()
        self.stdout.write(
            self.style.SUCCESS(
                'Extracting products from Open Food Facts website...'
            )
        )
        html = urlopen(self.BASE_URL)

        soup = BeautifulSoup(html, 'html.parser')

        results = soup.find(id='search_results').find_all('li')

        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(get_soup_product_detail, url)
                for url in get_products_url(results)
            ]
            for future in as_completed(futures):
                try:
                    update_or_create_product(*future.result())
                except HTTPError as error:
                    sentry_sdk.capture_message(
                        f'API Open Food Facts error: {error}', 'error'
                    )
                    continue

        end_time = datetime.now()
        self.stdout.write(
            self.style.SUCCESS(
                'Extracting products from Open Food Facts website done in '
                f'{end_time - initial_time}'
            )
        )
