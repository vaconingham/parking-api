from parking.models import CarPark, Bay
from rest_framework import status
from model_bakery import baker
import pytest


@pytest.mark.django_db
class TestCreateBays:
    def test_if_create_bay_returns_201(self, api_client):
        car_park = baker.make(CarPark)
        response = api_client.post(f'/car-parks/cp/{car_park.pk}/bays/add/', { 'car_park': car_park.pk })
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['bay_number'] == len(Bay.objects.all())
    
    def test_if_invalid_data_returns_400(self, api_client):
        car_park = baker.make(CarPark)
        response = api_client.post(f'/car-parks/cp/{car_park.pk}/bays/add/', { 'car_park': "" })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['car_park'] is not None
    
    @pytest.mark.skip
    def test_if_bay_number_conflicts_returns_400(self, api_client):
        car_park = baker.make(CarPark)
        api_client.post('/car-parks/cp/<int:pk>/bays/add/', { 'car_park': car_park.pk, "bay_number": 1 })
        response = api_client.post('/car-parks/cp/<int:pk>/bays/add/', { 'car_park': car_park.pk, "bay_number": 1 })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        

@pytest.mark.django_db
class TestRetrieveBays:
    def test_if_bay_exists_returns_200(self, api_client):
        bay = baker.make(Bay)
        response = api_client.get(f'/car-parks/cp/{bay.car_park.pk}/bays/bay/{bay.bay_number}/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteBays:
    def test_if_delete_bay_returns_204(self, api_client):
        bay = baker.make(Bay)
        response = api_client.delete(f'/car-parks/cp/{bay.car_park.pk}/bays/bay/{bay.bay_number}/delete/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
