"""fcote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "CoteEdu Admin"
admin.site.site_title = "CoteEdu  Admin Site"
admin.site.index_title = "CoteEdu  Admin"
urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/account/", include("Account.urls")),
    path("api/assignment/", include("Assignment.urls")),
    path("api/challenge/", include("Challenge.urls")),
    path("api/group/", include("Group.urls")),
    # path("api/submit/", include("Submit.urls")),
]
