import re
from typing import Sequence, Tuple, Union
from urllib.parse import urljoin
from urllib.request import urlopen

import sentry_sdk
from bs4 import BeautifulSoup
from django.db.utils import DataError

from fitness_food.products.models import Brand, Category, Packaging, Product


def get_soup_product_detail(url: str) -> Tuple[int, str, BeautifulSoup]:
    """
    Retrieves the product details from a given URL.
    Returns a tuple containing the code, URL, and BeautifulSoup object of
    the product page.
    """
    code = int(re.search(r'(?<=\/)\d+(?=\/)', url).group())
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    return code, url, soup


def get_products_url(results: list) -> Sequence[str]:
    """
    Get products url from BeautifulSoup object.
    """
    for li in results:
        yield urljoin('https://world.openfoodfacts.org', li.a['href'])


def get_barcode_from_soup(soup: BeautifulSoup, code: int) -> Union[str, None]:
    """
    Get barcode from BeautifulSoup object.
    """
    try:
        barcode_paragraph = soup.find(id='barcode_paragraph').text
        return re.search(r'\d+.*\)', barcode_paragraph).group()
    except AttributeError:
        sentry_sdk.capture_message(
            f'Failed to get barcode for product {code}.', 'error'
        )
        return None


def get_name_from_soup(soup: BeautifulSoup, code: int) -> Union[str, None]:
    """
    Get name from BeautifulSoup object.
    """
    try:
        return soup.find(property='food:name').text
    except AttributeError:
        sentry_sdk.capture_message(
            f'Failed to get name for product {code}.', 'error'
        )
        return None


def get_quantity_from_soup(soup: BeautifulSoup, code: int) -> Union[str, None]:
    """
    Get quantity from BeautifulSoup object.
    """
    try:
        return soup.find(id='field_quantity_value').text
    except AttributeError:
        sentry_sdk.capture_message(
            f'Failed to get quantity for product {code}.', 'error'
        )
        return None


def get_packaging_from_soup(soup: BeautifulSoup, code: int) -> list:
    """
    Get list of instances of packaging from BeautifulSoup object.
    """
    try:
        packaging = soup.find(id='field_packaging_value').text.split(', ')
        return [
            Packaging.objects.get_or_create(name=p.strip())[0]
            for p in packaging
        ]
    except (AttributeError, DataError):
        sentry_sdk.capture_message(
            f'Failed to get packaging for product {code}.', 'error'
        )
        return []


def get_categories_from_soup(soup: BeautifulSoup, code: int) -> list:
    """
    Get list of instances of categories from BeautifulSoup object.
    """
    try:
        categories = soup.find(id='field_categories_value').text.split(', ')
        return [
            Category.objects.get_or_create(name=c.strip())[0]
            for c in categories
        ]
    except (AttributeError, DataError):
        sentry_sdk.capture_message(
            f'Failed to get categories for product {code}.', 'error'
        )
        return []


def get_brands_from_soup(soup: BeautifulSoup, code: int) -> list:
    """
    Get list of instances of brands from BeautifulSoup object.
    """
    try:
        brands = soup.find(id='field_brands_value').text.split(', ')
        return [Brand.objects.get_or_create(name=b.strip())[0] for b in brands]
    except (AttributeError, DataError):
        sentry_sdk.capture_message(
            f'Failed to get brands for product {code}.', 'error'
        )
        return []


def update_or_create_product(
    code: int, url: str, soup: BeautifulSoup
) -> Product:
    """
    Create or update a product from code, url and BeautifulSoup object.
    """
    try:
        product = Product.objects.get(code=code)
        if product.status == Product.StatusChoices.IMPORTED:
            return product
    except Product.DoesNotExist:
        product = Product()
        product.code = code
        product.status = Product.StatusChoices.DRAFT

    name = get_name_from_soup(soup, code)
    barcode = get_barcode_from_soup(soup, code)
    quantity = get_quantity_from_soup(soup, code)

    product.product_name = name
    product.barcode = barcode
    product.quantity = quantity
    product.url = url

    packaging = get_packaging_from_soup(soup, code)
    categories = get_categories_from_soup(soup, code)
    brands = get_brands_from_soup(soup, code)

    if all([name, barcode, quantity, packaging, categories, brands]):
        product.status = Product.StatusChoices.IMPORTED

    product.save()
    product.packaging.set(packaging)
    product.brands.set(brands)
    product.categories.set(categories)
    return product
