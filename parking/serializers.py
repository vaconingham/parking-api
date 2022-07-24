from rest_framework import serializers
from .models import CarPark, Bay, Customer, Reservation


class BayListField(serializers.RelatedField):
    def to_representation(self, value):
        return f"{value.bay_number} - Type: {value.bay_type}"


class CustomerNameField(serializers.RelatedField):
    def to_representation(self, value):
        return value.customer_name


class BaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bay
        fields = [
            'bay_number',
            'car_park',
            'bay_type',
            'created',
            'updated',
        ]


class CarParkSerializer(serializers.ModelSerializer):
    bays = BayListField(many=True, read_only=True)

    class Meta:
        model = CarPark
        fields = [
            'pk',
            'name',
            'abn',
            'address',
            'phone',
            'email',
            'website',
            'bays',
            'number_of_bays',
            'created',
            'updated',
            ]
    
    def update(self, instance):
        instance.number_of_bays = len(Bay.objects.filter(car_park=self.pk))
        return instance


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    # vehicle_registration = serializers.CharField(max_length=10, source="customer")
    class Meta:
        model = Reservation
        fields = [
            'date',
            'car_park',
            'bay',
            'customer',
            'created',
            'updated',
        ]
