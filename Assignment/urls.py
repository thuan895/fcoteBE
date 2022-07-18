from django.urls import path
from .views import *

urlpatterns = [
    path('get-assignment-tag', getAssignmentTag),
    path('get-language', getLanguage),
    path('get-data-type', getDataType),
    path('get-list-assignment', getListAssignment),
    path('get-assignment-detail', getAssignmentDetail),
    path('add-assignment', addAssignment),
    path('delete-assignment', deleteAssignment),

]
