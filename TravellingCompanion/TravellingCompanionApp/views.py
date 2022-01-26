from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, Trip, City, CitiesForTrips
from uuid import uuid4
import operator
from typing import List


# region Private functions

def get_all_trips_for_user(user_id: str):
    """
    Method that gets all trips for particular user id
    :param user_id: user id of user to search trips for
    :return: list of trips
    """
    try:
        trips = Trip.objects.filter(user_id=user_id)
        trips = sorted(trips, key=operator.attrgetter('trip_date'))
    except Trip.DoesNotExist:
        trips = []
    return trips


def get_all_trips_for_user_and_its_cities(user_id: str):
    """
    Method that gets all trips with its destinations for particular user id
    :param user_id: user id of user to search trips for
    :return: list of trips with cities
    """
    trips_return = list()
    trips = get_all_trips_for_user(user_id)
    for trip in trips:
        cities_for_trip = CitiesForTrips.objects.filter(trip_id=trip.id)
        cities_names = [city.city_id.city_name for city in cities_for_trip]
        cities_names_concat = ",".join(cities_names)

        trip_dict = dict()
        trip_dict['id'] = trip.id
        trip_dict['associates'] = trip.associates
        trip_dict['trip_date'] = trip.trip_date
        trip_dict['total_cost'] = trip.total_cost
        trip_dict['destinations'] = cities_names_concat
        trips_return.append(trip_dict)

    return trips_return


def update_trip(trip_id: str, associates: str, trip_date: str, total_cost: int, selected_cities: List[str], user_id: str):
    """
    Method for updating particular trip
    :param trip_id: trip id of trip to update
    :param associates: associates for trip
    :param trip_date: date for trip
    :param total_cost: cost of a trip
    :param selected_cities: list of selected cities for trip
    :param user_id: user id that is making new trip
    :return: True if success else False
    """
    success = True
    try:
        trip = Trip.objects.get(id=trip_id)
        trip.associates = associates
        trip.trip_date = trip_date
        trip.total_cost = total_cost
        trip.user_id = user_id
        trip.save()

        CitiesForTrips.objects.filter(trip_id=trip_id).delete()
        for city_id in selected_cities:
            id = str(uuid4())
            city = City.objects.get(id=city_id)
            CitiesForTrips.objects.create(id=id, trip_id=trip, city_id=city)
    except Exception as e:
        success = False
    return success


# endregion

# region views

def index(request):
    """
    Method for redirecting on index page
    :param request: request
    :return: index page
    """
    return render(request, 'TravellingCompanionApp/index.html')


def register(request):
    """
    Method for redirecting on register page
    :param request: request
    :return: register page
    """
    return render(request, 'TravellingCompanionApp/register.html')


def user_menu(request):
    """
    Method for redirecting on user_menu page
    :param request: request
    :return: user_menu page
    """
    user_id = request.session['user_id']
    trips = get_all_trips_for_user_and_its_cities(user_id)
    return render(request, 'TravellingCompanionApp/user_menu.html', {'trips': trips})


def add_new_trip(request):
    """
    Method for redirecting on add_new_trip page
    :param request: request
    :return: add_new_trip page
    """
    return render(request, 'TravellingCompanionApp/add_new_trip.html')


def add_new_destination(request):
    """
    Method for redirecting on add_new_destination page
    :param request: request
    :return: add_new_destination page
    """
    return render(request, 'TravellingCompanionApp/add_new_destination.html')


# endregion

# region API Endpoints

def login(request):
    """
    Method for providing login
    :param request: request
    :return: user_menu page if successful else redirect to index
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        user = User.objects.get(username=username, password=password)
        user_id = user.id
    except User.DoesNotExist:
        user_id = None

    if user_id is None:
        messages.info(request, 'User with defined credentials not existing')
        return render(request, 'TravellingCompanionApp/index.html')
    else:
        request.session['user_id'] = user_id
        trips = get_all_trips_for_user_and_its_cities(user_id)
        return render(request, 'TravellingCompanionApp/user_menu.html', {'trips': trips})


def register_user(request):
    """
    Method for providing user registration
    :param request: request
    :return: user_menu page if successful else redirect to index
    """
    id = str(uuid4())
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    date_of_birth = request.POST.get('birthday')
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')

    try:
        # already existing user
        user = User.objects.get(username=username)
        messages.info(request, 'User with same username already existing in database')
        return render(request, 'TravellingCompanionApp/index.html')
    except User.DoesNotExist:
        # not existing user with defined username
        User.objects.create(id=id, name=name, surname=surname, date_of_birth=date_of_birth, username=username,
                            password=password, email=email)
        request.session['user_id'] = id
        trips = get_all_trips_for_user_and_its_cities(id)
        return render(request, 'TravellingCompanionApp/user_menu.html', {'trips': trips})


def register_new_trip(request):
    """
    Method for providing adding new trip
    :param request: request
    :return: user_menu page if successful else redirect to same page
    """
    id = str(uuid4())
    user_id = request.session['user_id']

    associates = request.POST.get('associates')
    trip_date = request.POST.get('trip_date')
    total_cost = request.POST.get('total_cost')

    try:
        # trip for user on particular date already existing
        trip = Trip.objects.get(user_id=user_id, trip_date=trip_date)
        messages.info(request, 'Unable to add new trip since user is already traveling for particular day')
        return render(request, 'TravellingCompanionApp/add_new_trip.html')
    except Trip.DoesNotExist:
        # new trip for user to add
        Trip.objects.create(id=id, associates=associates, trip_date=trip_date, total_cost=total_cost, user_id=user_id)
        user_id = request.session.get('user_id')
        trips = get_all_trips_for_user_and_its_cities(user_id)
        return render(request, 'TravellingCompanionApp/user_menu.html', {'trips': trips})


def register_new_destination(request):
    """
    Method for providing adding new destination
    :param request: request
    :return: user_menu page if successful else redirect to same page
    """
    id = str(uuid4())

    city_name = request.POST.get('city_name')
    country = request.POST.get('country')
    population = request.POST.get('population')

    try:
        # check if city already in the database
        city = City.objects.get(city_name=city_name, country=country)
        messages.info(request, 'Destination not added as already existing')
        return render(request, 'TravellingCompanionApp/add_new_destination.html')
    except City.DoesNotExist:
        # write new city as it does not exist in the database
        City.objects.create(id=id, city_name=city_name, country=country, population=population)
        user_id = request.session.get('user_id')
        trips = get_all_trips_for_user_and_its_cities(user_id)
        return render(request, 'TravellingCompanionApp/user_menu.html', {'trips': trips})


def manage_trips(request):
    """
    Method for invoking page with possibilities for trips management
    :param request: request
    :return: list_of_trips page
    """
    user_id = request.session.get('user_id')
    trips = get_all_trips_for_user(user_id)
    return render(request, 'TravellingCompanionApp/list_of_trips.html', {'trips': trips})


def get_edit_data(request, trip_id):
    """
    Method for getting all required data for one trip
    :param request: request
    :param trip_id: trip id for data to fetch
    :return: manage_trip page
    """
    request.session['trip_id'] = trip_id
    trip = Trip.objects.get(id=trip_id)
    trip.associates = trip.associates.replace(' ', '')
    cities_for_trip = CitiesForTrips.objects.filter(trip_id=trip_id)
    cities_for_trip_ids = [item.city_id.id for item in cities_for_trip]

    cities = City.objects.all()
    cities_data = list()
    for city in cities:
        city_dict = dict()
        city_dict['city_id'] = city.id
        city_dict['city_name'] = city.city_name
        if city.id in cities_for_trip_ids:
            city_dict['selected'] = True
        else:
            city_dict['selected'] = False
        cities_data.append(city_dict)

    request.session['cities_data'] = cities_data
    return render(request, 'TravellingCompanionApp/manage_trip.html', {'trip': trip, 'cities_data': cities_data})


def modify_trip(request):
    """
    Method for updating desired trip
    :param request: request
    :return: return user_menu if successful else list_of_trips
    """
    cities_data = request.session['cities_data']
    trip_id = request.session['trip_id']
    user_id = request.session['user_id']

    associates = request.POST.get('associates')
    trip_date = request.POST.get('trip_date')
    total_cost = request.POST.get('total_cost')

    selected_cities = list()
    for item in cities_data:
        selected = request.POST.get(item['city_id'])
        if selected is not None:
            selected_cities.append(item['city_id'])

    success = update_trip(trip_id, associates, trip_date, total_cost, selected_cities, user_id)
    if success is True:
        # all data updated successfully
        messages.info(request, 'Trip successfully modified')
        user_id = request.session.get('user_id')
        trips = get_all_trips_for_user_and_its_cities(user_id)
        return render(request, 'TravellingCompanionApp/user_menu.html', {'trips': trips})
    else:
        # data update not updated successfully
        messages.info(request, 'Error while modifying trip')
        user_id = request.session.get('user_id')
        trips = get_all_trips_for_user(user_id)
        return render(request, 'TravellingCompanionApp/list_of_trips.html', {'trips': trips})


def delete_data(request, trip_id):
    """
    Method for deleting data for particular trip id
    :param request: request
    :param trip_id: id of a trip to delete
    :return: redirect to user_menu
    """
    trip = Trip.objects.filter(id=trip_id).delete()
    user_id = request.session.get('user_id')
    trips = get_all_trips_for_user(user_id)
    return redirect('/user_menu', trips=trips)

# endregion