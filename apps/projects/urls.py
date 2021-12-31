from django.contrib import admin
from django.urls import path, re_path, include

from projects import views
from rest_framework import routers

#生成路由集对象
router = routers.SimpleRouter()
router.register(r'projects', views.ProjectViewSet)

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('projects/<int:id>/', views.ProjectView.as_view()),
    path('projects/', views.ProjectViewSet.as_view({
        'post': 'create',
        'get': 'list'
    })),
    # path('projects/<int:id>/', views.ProjectView.as_view()),
    path('projects/<int:id>/', views.ProjectViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
        'patch': 'partial_update'
    })),
    # path('projects/<int:id>/interfaces/', views.ProjectViewSet.as_view({
    #     'get': 'interfaces',
    # })),
    # re_path('^projects/$', index),
    path('', include(router.urls))
]

# urlpatterns += router.urls