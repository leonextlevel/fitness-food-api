from django.urls import reverse


def test_root_view_status_code_200(client):
    response = client.get(reverse('root'))
    assert response.status_code == 200


def test_product_list_view_status_code_200(client, db):
    response = client.get(reverse('product-list'))
    assert response.status_code == 200


def test_product_detail_view_status_code_200(client, product_fixture):
    response = client.get(
        reverse('product-detail', kwargs={'code': product_fixture.code})
    )
    assert response.status_code == 200
