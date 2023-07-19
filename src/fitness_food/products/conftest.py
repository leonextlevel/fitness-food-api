import pytest
from model_bakery import baker


@pytest.fixture
def category_fixture(db):
    return baker.make('products.Category')


@pytest.fixture
def brand_fixture(db):
    return baker.make('products.Brand')


@pytest.fixture
def packaging_fixture(db):
    return baker.make('products.Packaging')


@pytest.fixture
def product_fixture(db):
    return baker.make('products.Product')
