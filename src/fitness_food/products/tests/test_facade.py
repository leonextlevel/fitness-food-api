from unittest.mock import MagicMock, patch

from fitness_food.products.facade import (
    get_barcode_from_soup,
    get_brands_from_soup,
    get_categories_from_soup,
    get_name_from_soup,
    get_packaging_from_soup,
    get_products_url,
    get_quantity_from_soup,
    get_soup_product_detail,
    update_or_create_product,
)
from fitness_food.products.models import Product


def test_get_soup_product_detail():
    url = 'http://test.com/test/123456/test1'
    with patch('fitness_food.products.facade.urlopen') as mock_urlopen:
        mock_urlopen.return_value = 'html'
        with patch('fitness_food.products.facade.BeautifulSoup') as mock_bs:
            bs_value = 1
            mock_bs.return_value = bs_value
            assert get_soup_product_detail(url) == (123456, url, bs_value)


def test_get_products_url_empty():
    assert list(get_products_url([])) == []


def test_get_products_url():
    mock_li = MagicMock()
    mock_li.a = {'href': '/teste/'}
    assert list(get_products_url([mock_li])) == [
        'https://world.openfoodfacts.org/teste/'
    ]


def test_get_barcode_from_soup_invalid_soup():
    soup = MagicMock()
    soup.find.return_value = ''
    assert get_barcode_from_soup(soup, 123456) is None


def test_get_barcode_from_soup():
    soup = MagicMock()
    soup.find.return_value = MagicMock()
    soup.find.return_value.text = 'Teste 123456 (test)'
    assert get_barcode_from_soup(soup, 123456) == '123456 (test)'


def test_get_name_from_soup_invalid_soup():
    soup = MagicMock()
    soup.find.return_value = ''
    assert get_name_from_soup(soup, 123456) is None


def test_get_name_from_soup():
    soup = MagicMock()
    soup.find.return_value = MagicMock()
    soup.find.return_value.text = 'Teste'
    assert get_name_from_soup(soup, 123456) == 'Teste'


def test_get_quantity_from_soup_invalid_soup():
    soup = MagicMock()
    soup.find.return_value = ''
    assert get_quantity_from_soup(soup, 123456) is None


def test_get_quantity_from_soup():
    soup = MagicMock()
    soup.find.return_value = MagicMock()
    soup.find.return_value.text = 'Teste'
    assert get_quantity_from_soup(soup, 123456) == 'Teste'


def test_get_packaging_from_soup(packaging_fixture):
    soup = MagicMock()
    soup.find.return_value = MagicMock()
    soup.find.return_value.text = packaging_fixture.name
    assert get_packaging_from_soup(soup, 123456) == [packaging_fixture]


def test_get_categories_from_soup(category_fixture):
    soup = MagicMock()
    soup.find.return_value = MagicMock()
    soup.find.return_value.text = category_fixture.name
    assert get_categories_from_soup(soup, 123456) == [category_fixture]


def test_get_brands_from_soup(brand_fixture):
    soup = MagicMock()
    soup.find.return_value = MagicMock()
    soup.find.return_value.text = brand_fixture.name
    assert get_brands_from_soup(soup, 123456) == [brand_fixture]


def test_update_or_create_product_already_imported(product_fixture):
    product_fixture.status = Product.StatusChoices.IMPORTED
    soup = MagicMock()
    soup.find.return_value = MagicMock()
    soup.find.return_value.text = 'Teste'
    assert (
        update_or_create_product(
            product_fixture.code, product_fixture.url, soup
        )
        == product_fixture
    )
