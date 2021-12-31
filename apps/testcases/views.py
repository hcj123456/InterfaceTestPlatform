import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from interfaces.models import Interfaces
from .models import Testcases
from .serializers import TestcaseModelSerializer
from utils.handle_datas import handle_data4, handle_data2


class TestcaseViewSet(ModelViewSet):
    """
    create: 创建项目
    list: 查询所有项目信息
    retrieve: 查询一条项目信息
    update: 全量更新
    partial_update: 部分更新
    destroy: 删除项目信息
    """
    queryset = Testcases.objects.all()
    serializer_class = TestcaseModelSerializer
    # filter_backends = [SearchFilter, OrderingFilter]
    filter_backends = [SearchFilter, OrderingFilter]
    # filterset_fields = ['name']
    # filterset_class = TimeFilterSet
    search_fields = ['name']
    ordering_fields = ['id']
    lookup_url_kwarg = 'id'
    authentication_classes = [JSONWebTokenAuthentication]
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        request_obj = self.get_object()
        request_dict = json.loads(request_obj.request, encoding='utf-8')
        #获取headers
        request_headers = request_dict['config']['request']['headers']
        request_headers_list = handle_data4(request_headers)

        #获取变量
        config_variables = request_dict['config'].get('variables')
        config_variables_list = handle_data2(config_variables)

        request_obj_name = request_obj.name
        request_obj_author = request_obj.author
        request_obj_interface_id = request_obj.interface.id
        request_obj_project_id = Interfaces.objects.get(id=request_obj_interface_id).project.id
        # request_obj_project_id = Projects.objects.get(interfaces__id=request_obj_interface_id).id

        data = {
            "configure_name": request_obj_name,
            'configure_author': request_obj_author,
            'configure_interface_id': request_obj_interface_id,
            'configure_interface_project_id': request_obj_project_id,
            'configure_headers': request_headers_list,
            'configure_variables': config_variables_list
        }
        return Response(data)