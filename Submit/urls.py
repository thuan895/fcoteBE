from django.urls import path
from .views import *

urlpatterns = [
    path('submit', submitAssignment),
    path('run', runAssignment),
]
