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
from testcases.models import Testcases
from configures.models import Configures
from .models import Interfaces
from .serializers import InterfaceModelSerializer, ConfiguresByInterfacesIdSerializer, TestcasesByInterfacesIdSerializer

# class InterfaceView(View):
#
#     def get(self, request, id):
#         # data = {
#         #     'name': 'mkmk',
#         #     'age': 18
#         # }
#         # obj = json.dumps(data, ensure_ascii=False)
#         # qs = Projects.objects.exclude(name="接口测试平台项目")
#         # qs = Interfaces.objects.create()
#         obj = Interfaces.objects.get(id=id)
#         serializer_obj = InterfaceModelSerializer(instance=obj)
#         # serializer_obj.is_valid(raise_exception=True)
#         # tt = []
#         # for obj in qs:
#         #     tt.append({
#         #         'name':obj.name,
#         #         'leader': obj.leader,
#         #         'desc': obj.desc
#         #     })
#         # obj = Projects.objects.get(name='接口测试平台项目')
#         # ob = {
#         #         'name': obj.name,
#         #         'leader': obj.leader,
#         #         'desc': obj.desc
#         #     }
#         return JsonResponse(serializer_obj.data, json_dumps_params={'ensure_ascii': False})
#
#     def post(self, request):
#         # obj = Projects(name='接口测试平台项目', leader='项目负责人', desc='非常好用的测试平台')
#         # obj.save()
#         data = request.body.decode('utf-8')
#         request_data = json.loads(data)
#         serializer_obj = InterfaceModelSerializer(data=request_data)
#         serializer_obj.is_valid(raise_exception=True)
#         obj = Interfaces.objects.create(**serializer_obj.validated_data)
#         # objs = {
#         #     "name" : obj.name,
#         #     "leader": obj.leader,
#         #     'desc': obj.desc
#         # }
#         serializer_obj1 = InterfaceModelSerializer(instance=obj)
#         return JsonResponse(serializer_obj1.data, json_dumps_params={'ensure_ascii': False})
#         # data = {
#         #     'name': 'mkmk',
#         #     'age': 18
#         # }
#         # tt = request.body.decode('utf-8')
#         # obj = json.loads(tt, encoding='utf-8')
#         # # obj = json.dumps(data, ensure_ascii=False)
#         # # return HttpResponse(obj)
#         # return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
#
#
#     def put(self, request):
#         return HttpResponse()
#
#     def delete(self, request):
#         return HttpResponse()
#
#     def patch(self, request):
#         return HttpResponse()
#
#
# class InterfacesModelView(View):
#     def get(self, request):
#         # data = {
#         #     'name': 'mkmk',
#         #     'age': 18
#         # }
#         # obj = json.dumps(data, ensure_ascii=False)
#         # qs = Projects.objects.exclude(name="接口测试平台项目")
#         # qs = Interfaces.objects.create()
#         obj = Interfaces.objects.all()
#         serializer_obj = InterfaceModelSerializer(instance=obj, many=True)
#         # serializer_obj.is_valid(raise_exception=True)
#         # tt = []
#         # for obj in qs:
#         #     tt.append({
#         #         'name':obj.name,
#         #         'leader': obj.leader,
#         #         'desc': obj.desc
#         #     })
#         # obj = Projects.objects.get(name='接口测试平台项目')
#         # ob = {
#         #         'name': obj.name,
#         #         'leader': obj.leader,
#         #         'desc': obj.desc
#         #     }
#         return JsonResponse(serializer_obj.data, safe=False, json_dumps_params={'ensure_ascii': False})
#
#     def post(self, request):
#         # obj = Projects(name='接口测试平台项目', leader='项目负责人', desc='非常好用的测试平台')
#         # obj.save()
#         data = request.body.decode('utf-8')
#         request_data = json.loads(data)
#         serializer_obj = InterfaceModelSerializer(data=request_data)
#         serializer_obj.is_valid(raise_exception=True)
#         serializer_obj.save()
#         # obj = Interfaces.objects.create(**serializer_obj.validated_data)
#         # objs = {
#         #     "name" : obj.name,
#         #     "leader": obj.leader,
#         #     'desc': obj.desc
#         # }
#         # serializer_obj1 = InterfaceModelSerializer(instance=obj)
#         return JsonResponse(serializer_obj.data, json_dumps_params={'ensure_ascii': False})
#         # data = {
#         #     'name': 'mkmk',
#         #     'age': 18
#         # }
#         # tt = request.body.decode('utf-8')
#         # obj = json.loads(tt, encoding='utf-8')
#         # # obj = json.dumps(data, ensure_ascii=False)
#         # # return HttpResponse(obj)
#         # return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


class InterfaceViewSet(ModelViewSet):
    """
    create: 创建项目
    list: 查询所有项目信息
    retrieve: 查询一条项目信息
    update: 全量更新
    partial_update: 部分更新
    destroy: 删除项目信息
    """
    queryset = Interfaces.objects.all()
    serializer_class = InterfaceModelSerializer
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

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        results = response.data['results']
        for item in results:
            testcase_count = Testcases.objects.filter(interface__id=item.get('id')).count()
            configure_count = Configures.objects.filter(interface__id=item.get('id')).count()
            item['testcases'] = testcase_count
            item['configures'] = configure_count
        return response

    @action(methods=['GET'], detail=True)
    def configures(self, request, *args, **kwargs):
        # obj = self.get_object()
        # serializer = self.get_serializer(instance=obj)
        result = super().retrieve(request, *args, **kwargs)
        results = result.data['configures']
        return Response(results)

    @action(methods=['GET'], detail=True)
    def testcases(self, request, *args, **kwargs):
        # obj = self.get_object()
        # serializer = self.get_serializer(instance=obj)
        result = super().retrieve(request, *args, **kwargs)
        results = result.data['testcases']
        return Response(results)

    def get_serializer_class(self):
        if self.action == 'configures':
            return ConfiguresByInterfacesIdSerializer
        elif self.action == 'testcases':
            return TestcasesByInterfacesIdSerializer
        else:
            return self.serializer_class

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     results = response.data['results']
    #     for item in results:
    #         testsuites_count = Testsuits.objects.filter(project__id=item.get('id')).count()
    #         testcases_count = Testcases.objects.filter(interface__project__id=item.get('id')).count()
    #         interfaces_count = Interfaces.objects.filter(project__id=item.get('id')).count()
    #         configures_count = Configures.objects.filter(interface__project__id=item.get('id')).count()
    #         item["interfaces"] = interfaces_count
    #         item["testcases"] = testcases_count
    #         item["testsuites"] = testsuites_count
    #         item["configures"] = configures_count
    #     return response
    #
    # @action(methods=['GET'], detail=False)
    # def names(self,request, *args,  **kwargs):
    #     qs = self.get_queryset()
    #     serializer_obj = self.get_serializer(instance=qs, many=True)
    #     return Response(serializer_obj.data, status=status.HTTP_200_OK)
    #
    # @action(methods=['GET'], detail=True)
    # def interfaces(self, request, *args, **kwargs):
    #     qs = self.get_object()
    #     serializer_obj = self.get_serializer(instance=qs)
    #     return Response(serializer_obj.data, status=status.HTTP_200_OK)
    #
    # # @action(methods=['GET'], detail=False)
    # # def selectrelated(self, request, *args, **kwargs):
    # #     # qs = Interfaces.objects.prefetch_related(Prefetch('', queryset=, to_attr=''))
    # #     # qs = Interfaces.objects.all()
    # #     # qs = Interfaces.objects.select_related('project').get(id=1)
    # #     qs = Interfaces.objects.get(id=1)
    # #     name = qs.name
    # #     project_name = qs.project.name
    # #     # qs = Interfaces.objects.filter(project__id=1)
    # #     # qs = Projects.objects.select_related('interfaces')
    # #     return Response(None)
    #
    # def get_serializer_class(self):
    #     if self.action == 'name':
    #         return ProjectNameModelSerializer
    #     elif self.action == 'interfaces':
    #         return ProjectInterfacesSerializer
    #     else:
    #         return self.serializer_class
    #
    # def paginate_queryset(self, queryset):
    #     if self.action == 'names':
    #         return None
    #     else:
    #         return super().paginate_queryset(queryset)
    #
    # def filter_queryset(self, queryset):
    #     if self.action == 'names':
    #         return queryset
    #     else:
    #         return super().filter_queryset(queryset)