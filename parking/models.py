import datetime
import logging
from django.db import models
from rest_framework import serializers

logger = logging.getLogger(__name__)

class CarPark(models.Model):
    name = models.CharField(max_length=50)
    abn = models.CharField(max_length=11, blank=True) # Validation required.
    address = models.CharField(max_length=100, blank=True) # Validation required.
    phone = models.CharField(max_length=30, blank=True) # Validation required.
    email = models.EmailField(max_length=50, blank=True)
    website = models.CharField(max_length=50, blank=True) #Validation requierd.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
        verbose_name = 'Car Park'
        verbose_name_plural = 'Car Parks'

    def __str__(self):
        return self.name

    @property
    def number_of_bays(self):
        return len(Bay.objects.filter(car_park=self.pk))
    
    @property
    def bays(self):
        return Bay.objects.filter(car_park=self.pk)
    
    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.full_clean()
        return super().save(*args, **kwargs)


def generate_bay_number(car_park):
    num = len(Bay.objects.filter(car_park=car_park)) + 1
    logger.info("NEW_BAY_NUMBER_GENERATED")
    return num

class Bay(models.Model):

    class VehicleType(models.TextChoices):
        MOTORCYCLE = 'MC'
        CAR = 'PC'
    
    car_park = models.ForeignKey(
        CarPark, 
        related_name='bay', 
        related_query_name='bays',
        on_delete=models.CASCADE
        )
    bay_type = models.CharField(
        max_length=2, 
        choices=VehicleType.choices, 
        default=VehicleType.CAR
        )

    bay_number = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_reserved = models.BooleanField(default=False)
    is_acrod = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        verbose_name = 'Vehicle Bay'
        verbose_name_plural = 'Vehicle Bays'

    def __int__(self):
        return self.bay_number
    
    def save(self, *args, **kwargs):
        self.bay_number = generate_bay_number(self.car_park)
        super(Bay, self).save(*args, **kwargs)


class Customer(models.Model):
    vehicle_registration = models.CharField(max_length=10, verbose_name='vehicle registration', primary_key=True) # Validation required.
    customer_name = models.CharField(max_length=50, verbose_name='customer name') # Validation required.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.vehicle_registration
    
    def save(self, *args, **kwargs):
        self.vehicle_registration = self.vehicle_registration.lower()
        self.customer_name = self.customer_name.lower()
        return super().save(*args, **kwargs)


class Reservation(models.Model):
    car_park = models.ForeignKey(CarPark, related_name='reservation', related_query_name='reservations', on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, 
        related_name='reservation', 
        related_query_name='reservations', 
        on_delete=models.CASCADE,
        )
    date = models.DateField()
    bay = models.ForeignKey(Bay, related_name='reservation', related_query_name='reservations', on_delete=models.CASCADE, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __int__(self):
        return f"{self.date} BAY {self.bay} @{self.car_park} RESERVED FOR {self.customer}"
    
    def allocate_bay(self):
        reservations = Reservation.objects.filter(car_park=self.car_park, date=self.date)
        if len(reservations) == len(Bay.objects.filter(car_park=self.car_park)):
            raise serializers.ValidationError("This car park is full on the requested date.")
        elif len(reservations) > 0 and len(reservations) <= len(Bay.objects.filter(car_park=self.car_park)):
            return Bay.objects.get(bay_number=len(reservations) + 1)
        else:
            return Bay.objects.get(bay_number=1)

    def clean(self):
        min_date = datetime.date.today() + datetime.timedelta(days=1)
        max_date = datetime.date.today() + datetime.timedelta(days=365)
        reservations = Reservation.objects.filter(car_park=self.car_park, date=self.date)
        customer_perm = True
        if len(reservations) > 0:
            for r in reservations:
                if self.customer == r.customer:
                    customer_perm = False
        if customer_perm != True:
            logger.info("CUSTOMER_ALREADY_BOOKED_DATE")
            raise serializers.ValidationError("Only one (1) booking allowed per vehicle per date.")
        if len(reservations) == len(Bay.objects.filter(car_park=self.car_park)):
            logger.info("CAR_PARK_IS_FULL")
            raise serializers.ValidationError("This car park is full on the requested date.")
        if self.date < min_date or self.date > max_date:
            logger.info("DATE_OUTSIDE_RANGE")
            raise serializers.ValidationError("A reservation cannot be within 24 hours or beyond 365 days of booking time.")

    def save(self, *args, **kwargs):
        self.bay = self.allocate_bay()
        self.full_clean()
        return super().save(*args, **kwargs)
