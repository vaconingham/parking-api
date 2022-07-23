from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from parking import views

router = routers.DefaultRouter()
# router.register('car-parks', views.ListCarParksView)

urlpatterns = [
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),

    path('car-parks/', views.ListCarParksView, name='list-all-car-parks'),
    path('car-parks/add/', views.ListCarParksView, name='add-cp'),
    path('car-parks/cp/<int:pk>/', views.CarParkView, name='cp-detail'),
    path('car-parks/cp/<int:pk>/delete/', views.CarParkView, name='delete-cp'),

    path('car-parks/cp/<int:pk>/bays/', views.ListBaysView, name='list-all-bays'),
    path('car-parks/cp/<int:pk>/bays/add/', views.ListBaysView,name='add-bay'),
    path('car-parks/cp/<int:pk>/bays/bay/<int:bay_number>/', views.BayView, name='bay-detail'),
    path('car-parks/cp/<int:pk>/bays/bay/<int:bay_number>/reservations/', views.BayReservationsListView, name='bay-all-reservations'),
    path('car-parks/cp/<int:pk>/bays/bay/<int:bay_number>/<str:date>/', views.BayDateView, name='bay-date-reserations'),
    path('car-parks/cp/<int:pk>/bays/bay/<int:bay_number>/delete/', views.BayView, name='delete-bay'),

    path('customers/', views.CustomersListView, name='list-all-customers/'),
    path('customers/add', views.CustomersListView, name='add-customers/'),
    path('customers/customer/<str:vehicle_registration>/', views.CustomerDetailView, name='customer-detail'),
    path('customers/customer/<str:vehicle_registration>/reservations/', views.CustomerReservationsListView, name='customer-reservations-list'), 
    path('customers/customer/<str:vehicle_registration>/delete/', views.CustomerDetailView, name='delete-customer'),

    # path('reservations/', view.AllReservationsListView),
    path('car-parks/cp/<int:pk>/reservations/', views.ReservationsListView, name='list-all-reservations'),
    path('car-parks/cp/<int:pk>/reservations/add/', views.ReservationsListView, name='add-reservation'), 
    path('car-parks/cp/<int:pk>/reservations/<str:date>/', views.ReservationsDateListView, name='date-reservations'),
    path('car-parks/cp/<int:pk>/reservations/<str:date>/reserved/', views.ReservedBayListView, name='date-reserved-bays'),
    path('car-parks/cp/<int:pk>/reservations/<str:date>/available/', views.AvailableBayListView, name='date-available-bays'),
    path('car-parks/cp/<int:pk>/reservations/<str:date>/reservation/<int:rpk>/', views.ReservationView, name='reservation-detail'),
    path('car-parks/cp/<int:pk>/reservations/<str:date>/reservation/<int:rpk>/delete/', views.ReservationView, name='delete-reservation'),
]
