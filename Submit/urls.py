from django.urls import path
from .views import *

urlpatterns = [
    path('get-list-group', getListGroup),
    path('get-group-detail', getGroupDetail),
    path('add-group', addGroup),
]
