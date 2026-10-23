from django.urls import path
from . import views


urlpatterns = [
    path(
        'create/',
        views.create_service,
        name='create_service'
    ),

    path(
        'list/',
        views.service_list,
        name='service_list'
    ),

    path(
        'edit/<int:service_id>/',
        views.edit_service,
        name='edit_service'
    ),

    path(
        'delete/<int:service_id>/',
        views.delete_service,
        name='delete_service'
    ),
]