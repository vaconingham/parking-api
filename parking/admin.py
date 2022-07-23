from django.contrib import admin
from .models import CarPark, Bay, Customer, Reservation

admin.site.register(CarPark)
admin.site.register(Bay)
admin.site.register(Customer)
admin.site.register(Reservation)
