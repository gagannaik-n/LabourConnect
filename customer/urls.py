from django.urls import path
from . import views

urlpatterns = [

    path(
        'create-profile/',
        views.create_customer_profile,
        name='create_customer_profile'
    ),

    path(
        'my-profile/',
        views.my_customer_profile,
        name='my_customer_profile'
    ),

    path(
        'dashboard/',
        views.customer_dashboard,
        name='customer_dashboard'
    ),

]