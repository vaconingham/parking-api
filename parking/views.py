from .models import CarPark, Bay, Customer, Reservation
from .serializers import CarParkSerializer, BaySerializer, CustomerSerializer, ReservationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Car Park:
@api_view(['GET', 'POST'])
def ListCarParksView(request):
    if request.method == 'GET':
        car_parks = CarPark.objects.all()
        serializer = CarParkSerializer(car_parks, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CarParkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def CarParkView(request, pk):
    try:
        car_park = CarPark.objects.get(pk=pk)
    except CarPark.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CarParkSerializer(car_park)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CarParkSerializer(car_park, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        car_park.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Bays:
@api_view(['GET', 'POST'])
def ListBaysView(request, pk):
    if request.method == 'GET':
        bays = Bay.objects.filter(car_park=pk)
        serializer = BaySerializer(bays, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def BayView(request, pk, bay_number):
    try:
        bay = Bay.objects.get(bay_number=bay_number, car_park=pk)
    except Bay.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BaySerializer(bay)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BaySerializer(bay, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        bay.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def BayReservationsListView(request, pk, bay_number):
    reservations = Reservation.objects.filter(car_park=pk, bay=bay_number)
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def BayDateView(request, pk, bay_number, date):
    reservations = Reservation.objects.filter(car_park=pk, bay=bay_number, date=date)
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)


# Customers:
@api_view(['GET', 'POST'])
def CustomersListView(request):
    if request.method == 'GET':
        customers = Customer.objects.all() # Conifgure to return only customers that have been to specific car_park
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def CustomerDetailView(request, vehicle_registration):
    try:
        customer = Customer.objects.get(pk=vehicle_registration)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def CustomerReservationsListView(request, vehicle_registration):
    if request.method == 'GET':
        reservations = Reservation.objects.filter(customer=vehicle_registration)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)


# Reservations:
@api_view(['GET', 'POST'])
def ReservationsListView(request, pk):
    if request.method == 'GET':
        reservations = Reservation.objects.filter(car_park=pk)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def ReservationView(request, pk, date, rpk):
    try:
        reservation = Reservation.objects.get(car_park=pk, pk=rpk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def ReservationsDateListView(request, pk, date):
    reservations = Reservation.objects.filter(car_park=pk, date=date)
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ReservedBayListView(request, pk, date):
    bays = Bay.objects.filter(car_park=pk)
    reservations = Reservation.objects.filter(car_park=pk, date=date)
    reserved = []
    for reservation in reservations:
        for bay in bays:
            if bay.bay_number == reservation.bay.bay_number:
                reserved.append(bay)

    serializer = BaySerializer(reserved, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def AvailableBayListView(request, pk, date):
    bays = Bay.objects.filter(car_park=pk)
    reservations = Reservation.objects.filter(car_park=pk, date=date)
    available = []
    for reservation in reservations:
        for bay in bays:
            if bay.bay_number != reservation.bay.bay_number:
                available.append(bay)

    serializer = BaySerializer(available, many=True)
    return Response(serializer.data)