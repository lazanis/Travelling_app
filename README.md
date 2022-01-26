# Travelling_companion

###Docker Run:
docker image build -t travelling-companion .

docker-compose run travelling-companion python TravellingCompanion/manage.py migrate
 
docker-compose up


###Starting Project:

command for making migration - python manage.py makemigrations

command for data migration - python manage.py migrate

command for running the app - python manage.py runserver

command for running the tests - python manage.py test


###API Endpoints:

The list of API Endpoints are in the urls.py file, bellow is explained each endpoint.

/login - function for user login (arguments are username and password)

/register_user - function for user registration

/register_new_trip - function for adding new Trip in the list of trips.

/register_new_destination - function for adding new Destination in the list of destinations.

/manage_trips - function for getting list of trips related to current user.

/get_edit_data - function for getting all the data for selected trip Id.

/modify_trip - function for updating selected trip.

/delete_data - function for deleting selected trip.

