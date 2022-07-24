from parking.models import CarPark
from rest_framework import status
from model_bakery import baker
import pytest


@pytest.mark.django_db
class TestCreateCarPark:
    def test_if_create_car_park_returns_201(self, api_client):
        # api_client.force_authenticate(user={})
        response = api_client.post('/car-parks/add/', { 'name': 'a' })
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_if_invalid_data_returns_400(self, api_client):
        response = api_client.post('/car-parks/add/', { 'name': "" })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None


@pytest.mark.django_db
class TestRetrieveCarPark:
    def test_if_car_park_exists_returns_200(self, api_client):
        car_park = baker.make(CarPark)
        response = api_client.get(f'/car-parks/cp/{car_park.pk}/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteCarPark:
    def test_if_delete_car_park_returns_204(self, api_client):
        car_park = baker.make(CarPark)
        response = api_client.delete(f'/car-parks/cp/{car_park.pk}/delete/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
