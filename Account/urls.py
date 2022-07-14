from django.urls import path, re_path
from .views import *
urlpatterns = [
    path('post-sign-up', postsignUp),
    path('post-sign-in', postsignIn),
    path('post-reset', postReset),
    path('get-profile', getProfile),
    path('put-avatar', putAvatar),
    path('get-image', getImage),
    path('update-profile', updateProfile),
    path('get-ranking', getRanking)
]
