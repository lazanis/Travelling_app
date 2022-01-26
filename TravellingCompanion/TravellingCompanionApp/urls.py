from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('register_user', views.register_user, name='register_user'),
    path('add_new_trip', views.add_new_trip, name='add_new_trip'),
    path('register_new_trip', views.register_new_trip, name='register_new_trip'),
    path('add_new_destination', views.add_new_destination, name='add_new_destination'),
    path('register_new_destination', views.register_new_destination, name='register_new_destination'),
    path('manage_trips', views.manage_trips, name='manage_trips'),
    path('get_edit_data/<str:trip_id>', views.get_edit_data, name='get_edit_data'),
    path('delete_data/<str:trip_id>', views.delete_data, name='delete_data'),
    path('user_menu', views.user_menu, name='user_menu'),
    path('modify_trip', views.modify_trip, name='modify_trip'),
    # path('user/<str:id>', views.get_user_by_id, name='get_user_by_id')
]
