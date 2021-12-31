from django.contrib import admin
from django.urls import path, re_path, include

from interfaces import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('projects/<int:id>/', views.ProjectView.as_view()),
    path('interfaces/<int:id>/', views.InterfaceViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('interfaces/', views.InterfaceViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('interfaces/<int:id>/configures/', views.InterfaceViewSet.as_view({
        'get': 'configures'
    })),
    path('interfaces/<int:id>/testcases/', views.InterfaceViewSet.as_view({
        'get': 'testcases'
    }))
    # re_path('^projects/$', index),
]