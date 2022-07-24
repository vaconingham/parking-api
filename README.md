# Parking App

This a simple API to handle all-day parking reservations at one or more car parks.

Created with the help of Django and the Django Rest Framework.

## Getting started

1. Clone the project
2. Crate a virtual environment: `python3 install venv path/to/your/virtual/env`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the development server: `python3 manage.py runserver`
5. To see all the API endpoints, open a browser and visit 127.0.0.1.

### Create a car park
Endpoint: `/car-parks/add`
POST: `{"name": "yourCarParkNameString"}`
Optional: abn:int, address:string, phone:string, email:string, website:string

### Add bays to your car park
Endpoint: `/car-parks/cp/yourCarParkPK/bays/add`
POST: `{"car_park": yourCarParkPkInt}`
Optional: bay_type:string

### Add a customer
Endpoint: `/car-parks/cp/yourCarParkPK/customers/add`
POST: `{"vehicle_registration": "regoString", "customerName": "customerNameString"}`

### Create a reservation
Endpoint: `carparks/cp/yourCarParkPK/reservations/add`
POST: `{"car_park": carParkPkInt, "customer": "CarRegoString", "date": "YYYY-MM-DD"}`
Optional: bay:int

* The number of reservations on a given date will be limited to the number of bays related to a specific car park.
* Creating a bay will automatically allocate a bay number.
* If a bay number is not provided at registration, the customer will be allocated a bay automatically.
* A customer can only make one booking per day. This is based on the vehicle registration number.

## To-Dos, Features & Edge Cases

### Critical:
- Hyperlinked API related fields
- Create viewsets
- Register router endpoints
- Get, update, or create customer when creating reservation

### Coming Soon:
- list of available dates within date range
- List partially reserved dates
- Configure timezones
- Configure better date and time formats
- Create OpenAPI document
- Allow customer to choose any bay
- Allow car park and/or bays to be unavailable/closed on specific days e.g. weekends
- Allow booking of multiple days
- Allow bookings of time periods e.g. 12hours, 24hours, week, etc.
- Change time of booking contraints e.g. bookings can be made further into the future or within less/more time.

## Tests

Automated testing done using PyTest. You can find all the different tests inside the 'tests' directory.

Validation tests include:
- Customer vehicle registrations must be unique unique
- Reservation cannot be made within 24 hours of booking.
- Reservation cannot be made beyond 365 days of booking.
- Reservation cannot be made on date where car park is full.
- Reservation cannot be made if customer already exists on date.

## Bugs

- Customers don't belong to any particular carpark
- Get or create customer on reservation

## Current constraints

- A day is considered a calendar day and not a "24 hour period".
- A reservation cannot be made within 24 hours.
- A reservation cannot be made beyond 365 days.
- Customers can call themselves whatever they want.

## Contributing

If you would like to make a contribution, simply fork the project and submit a pull request to the `main` branch.
