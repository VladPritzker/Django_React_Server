from django.urls import path
from myapp.views import users  # make sure to import the combined function

urlpatterns = [
    path('users/', users, name='users'),  # Updated to use the combined 'users' function
]
