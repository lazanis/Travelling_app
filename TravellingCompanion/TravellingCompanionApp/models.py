from django.db import models


class User(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField('Date of birth')
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)


class Trip(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    associates = models.CharField(max_length=100)
    trip_date = models.DateField('Trip date')
    total_cost = models.IntegerField()


class City(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    city_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    population = models.IntegerField()


class CitiesForTrips(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
