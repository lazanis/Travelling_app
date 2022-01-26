from django.test import TestCase
from .models import User, Trip, City, CitiesForTrips


# Create your tests here.
class EndpointsTests(TestCase):
    def test_root(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_add_new_trip(self):
        response = self.client.get('/add_new_trip')
        self.assertEqual(response.status_code, 200)

    def test_add_new_destination(self):
        response = self.client.get('/add_new_destination')
        self.assertEqual(response.status_code, 200)

    def test_manage_trips(self):
        response = self.client.get('/manage_trips')
        self.assertEqual(response.status_code, 200)


class InstancesTests(TestCase):
    def setUp(self):
        User.objects.create(id='1', name='test1', surname='test1', date_of_birth='2020-01-01', username='test1', password='test1', email='test1')
        User.objects.create(id='2', name='test2', surname='test2', date_of_birth='2020-01-02', username='test2', password='test2', email='test2')

        t1 = Trip.objects.create(id='trip1', associates='test1,test2', trip_date='2022-01-01', total_cost=300, user_id='1')

        c1 = City.objects.create(id='city1', city_name='city1', country='country1', population=100)
        c2 = City.objects.create(id='city2', city_name='city2', country='country2', population=200)

        CitiesForTrips.objects.create(id='connection1', city_id=c1, trip_id=t1)
        CitiesForTrips.objects.create(id='connection2', city_id=c2, trip_id=t1)

    def test_user_login(self):
        user = User.objects.get(username='test1', password='test1')
        self.assertEqual(user.id, '1')

    def test_trips_for_user(self):
        trips = Trip.objects.filter(user_id='1')
        trip_ids = [trip.id for trip in trips]
        print(trip_ids)
        self.assertEqual(trip_ids, ['trip1'])

    def test_get_city_by_name_and_country(self):
        city = City.objects.get(city_name='city1', country='country1')
        self.assertEqual(city.id, 'city1')

    def test_get_cities_for_trip(self):
        cities_for_trip = CitiesForTrips.objects.filter(trip_id='trip1')
        cities_ids = [city.city_id.city_name for city in cities_for_trip]
        self.assertEqual(cities_ids, ['city1', 'city2'])
