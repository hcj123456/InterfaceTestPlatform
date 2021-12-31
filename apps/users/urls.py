from django.contrib import admin
from django.urls import path, re_path, include

from users import views
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    path('login/', obtain_jwt_token),
    #URLPathVersioning
    # re_path(r'^(?P<version>[v1|v2|v3]+)/users/register/$', views.UserViews.as_view({
    #     'post': 'create'
    # })),
    #QueryParameterVersioning
    # path('users/register/', views.UserViews.as_view({
    #     'post': 'create'
    # })),
    path('register/', views.UserViews.as_view({
        'post': 'create'
    })),
    re_path(r'^(?P<email>[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+)/count/$', views.UserViews.as_view({
        'get': 'check_email'
    })),
]