from django.urls import path
from . import views

urlpatterns = [

    path(
        'create-profile/',
        views.create_labor_profile,
        name='create_labor_profile'
    ),

    path(
        'edit-profile/',
        views.edit_labor_profile,
        name='edit_labor_profile'
    ),

    path(
        'my-profile/',
        views.my_labor_profile,
        name='my_labor_profile'
    ),

    path(
        'list/',
        views.labor_list,
        name='labor_list'
    ),

    path(
        '<int:labor_id>/',
        views.labor_detail,
        name='labor_detail'
    ),


    path(
         'dashboard/',
         views.labor_dashboard,
         name='labor_dashboard'
     ),
]