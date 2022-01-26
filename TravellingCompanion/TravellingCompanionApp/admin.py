from django.contrib import admin

# Register your models here.
from .models import User, Trip, City, CitiesForTrips
admin.site.register(User)
admin.site.register(Trip)
admin.site.register(City)
admin.site.register(CitiesForTrips)
