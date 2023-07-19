def test_product_image_url_barcode_length_less_or_equal_8(product_fixture):
    product_fixture.barcode = '12345678'
    product_fixture.save()
    assert product_fixture.image_url == (
        'https://images.openfoodfacts.org/images/products/'
        f'{product_fixture.barcode}/1.jpg'
    )


def test_product_image_url_barcode_length_more_8(product_fixture):
    product_fixture.barcode = '1234567891234'
    product_fixture.save()
    assert product_fixture.image_url == (
        'https://images.openfoodfacts.org/images/products/'
        '123/456/789/1234/1.jpg'
    )


def test_product_image_url_without_barcode(product_fixture):
    product_fixture.barcode = None
    product_fixture.save()
    assert product_fixture.image_url is None
