from django.urls import path
from .views import *

urlpatterns = [
    path('get-list-group', getListGroup),
    path('get-group-detail', detailGroup),
    path('create-group', createGroup),
    path('delete-group', deleteGroup),
    path('join-group', joinGroup),
]
