from django.urls import path
from .views import *

urlpatterns = [
    path('get-list-challenge', getListChallenge),
    path('get-detail-challenge', getDetailChallenge),
    path('create-challenge', createChallenge),
    path('delete-challenge', deleteChallenge),
]
