from parking.models import Customer
from rest_framework import status
from model_bakery import baker
import pytest


@pytest.mark.django_db
class TestCreateCustomer:
    def test_if_create_customer_returns_201(self, api_client):
        response = api_client.post(f'/customers/add/', { 'vehicle_registration': 'a', 'customer_name': 'b' })
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_if_invalid_data_returns_400(self, api_client):
        response = api_client.post(f'/customers/add/', { 'vehicle_registration': '', 'customer_name': '' })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['vehicle_registration'] is not None
        assert response.data['customer_name'] is not None
    
    def test_if_customer_already_exists_returns_400(self, api_client):
        api_client.post(f'/customers/add/', { 'vehicle_registration': 'a', 'customer_name': 'b' })
        response = api_client.post(f'/customers/add/', { 'vehicle_registration': 'a', 'customer_name': 'c' })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestRetrieveCustomer:
    def test_if_customer_exists_returns_200(self, api_client):
        customer = baker.make(Customer)
        response = api_client.get(f'/customers/customer/{customer.pk}/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDeleteCustomer:
    def test_if_delete_customer_returns_204(self, api_client):
        customer = baker.make(Customer)
        response = api_client.delete(f'/customers/customer/{customer.pk}/delete/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
