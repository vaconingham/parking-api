from parking.models import CarPark, Bay, Customer, Reservation
from rest_framework import status
from model_bakery import baker
import pytest
import datetime


@pytest.mark.django_db
class TestCreateReservation:
    def test_if_create_reservation_returns_201(self, api_client):
        car_park = baker.make(CarPark)
        customer = baker.make(Customer)
        date = datetime.date.today() + datetime.timedelta(days=1)
        api_client.post(f'/car-parks/cp/{car_park.pk}/bays/add/', { 'car_park': car_park.pk })
        response = api_client.post(f'/car-parks/cp/{car_park.pk}/reservations/add/', { 'car_park': 1, 'customer': customer.pk, 'date': date })
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_if_create_reservation_within_24_hours_returns_400(self, api_client):
        car_park = baker.make(CarPark)
        customer = baker.make(Customer)
        api_client.post(f'/car-parks/cp/{car_park.pk}/bays/add/', { 'car_park': car_park.pk })
        response = api_client.post(f'/car-parks/cp/{car_park.pk}/reservations/add/', { 'car_park': 1, 'customer': customer.pk, 'date': datetime.date.today() })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_if_create_reservation_past_365_days_returns_400(self, api_client):
        car_park = baker.make(CarPark)
        customer = baker.make(Customer)
        date = datetime.date.today() + datetime.timedelta(days=366)
        api_client.post(f'/car-parks/cp/{car_park.pk}/bays/add/', { 'car_park': car_park.pk })
        response = api_client.post(f'/car-parks/cp/{car_park.pk}/reservations/add/', { 'car_park': 1, 'customer': customer.pk, 'date': date })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_if_create_reservation_on_same_date_returns_400(self, api_client):
        car_park = baker.make(CarPark)
        customer = baker.make(Customer)
        date = datetime.date.today() + datetime.timedelta(days=1)
        api_client.post(f'/car-parks/cp/{car_park.pk}/bays/add/', { 'car_park': car_park.pk })
        api_client.post(f'/car-parks/cp/{car_park.pk}/bays/add/', { 'car_park': car_park.pk })
        api_client.post(f'/car-parks/cp/{car_park.pk}/reservations/add/', { 'car_park': 1, 'customer': customer.pk, 'date': date })
        response = api_client.post(f'/car-parks/cp/{car_park.pk}/reservations/add/', { 'car_park': 1, 'customer': customer.pk, 'date': date })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_if_create_reservation_car_park_full_returns_400(self, api_client):
        date = datetime.date.today() + datetime.timedelta(days=1)
        car_park = baker.make(CarPark)
        customer_yung = baker.make(Customer)
        customer_ling = baker.make(Customer)
        customer_yo = baker.make(Customer)
        api_client.post(f'/car-parks/cp/{car_park.pk}/bays/add/', { 'car_park': car_park.pk })
        api_client.post(f'/car-parks/cp/{car_park.pk}/bays/add/', { 'car_park': car_park.pk })
        api_client.post(f'/car-parks/cp/{car_park.pk}/reservations/add/', { 'car_park': car_park.pk, 'customer': customer_yung.pk, 'date': date })
        api_client.post(f'/car-parks/cp/{car_park.pk}/reservations/add/', { 'car_park': car_park.pk, 'customer': customer_ling.pk, 'date': date })
        response = api_client.post(f'/car-parks/cp/{car_park.pk}/reservations/add/', { 'car_park': car_park.pk, 'customer': customer_yo.pk, 'date': date })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveReservations:
    def test_if_reservation_list_exists_returns_200(self, api_client):
        date = datetime.date.today() + datetime.timedelta(days=1)
        car_park = baker.make(CarPark)
        customer = baker.make(Customer)
        api_client.post(f'/car-parks/cp/{car_park.pk}/bays/add/', { 'car_park': car_park.pk })
        api_client.post(f'/car-parks/cp/{car_park.pk}/reservations/add/', { 'car_park': car_park.pk, 'customer': customer.pk, 'date': date })
        response = api_client.get(f'/car-parks/cp/{car_park.pk}/reservations/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteReservation:
    def test_if_reservation_list_exists_returns_204(self, api_client):
        date = datetime.date.today() + datetime.timedelta(days=1)
        car_park = baker.make(CarPark)
        customer = baker.make(Customer)
        api_client.post(f'/car-parks/cp/{car_park.pk}/bays/add/', { 'car_park': car_park.pk })
        api_client.post(f'/car-parks/cp/{car_park.pk}/reservations/add/', { 'car_park': car_park.pk, 'customer': customer.pk, 'date': date })
        response = api_client.delete(f'/car-parks/cp/{car_park.pk}/reservations/{date}/reservation/1/delete/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
