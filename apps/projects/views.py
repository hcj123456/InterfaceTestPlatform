import json
from itertools import count

from django.db.models import Q, Prefetch, Count
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.db import connection
from rest_framework.decorators import action

from .models import Projects
from interfaces.models import Interfaces
from .serializers import ProjectModelSerializer, ProjectNameModelSerializer, ProjectInterfacesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from utils.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from utils.filterset import TimeFilterSet
from rest_framework import mixins, generics
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet
import logging
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from testsuites.models import Testsuits
from testcases.models import Testcases
from configures.models import Configures

logger = logging.getLogger('mytest')
logger.debug('你是爱我的')
logger.info('不，我不爱你')


# def index(request, id):
#     if request.method == "GET":
#         return HttpResponse(f"这是一个{id}奇妙的世界哦")
#     elif request.method == "POST":
#         return HttpResponse(f"这是一个{id}不太友好的世界")
#     else:
#         pass


# class ProjectView(View):
# class ProjectView(APIView):
# class ProjectView(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   GenericAPIView):
# class ProjectView(generics.CreateAPIView,
#                   generics.ListAPIView):
# class ProjectView(generics.ListCreateAPIView):
#     queryset = Projects.objects.all()
#     serializer_class = ProjectModelSerializer
#     # filter_backends = [SearchFilter, OrderingFilter]
#     filter_backends = [DjangoFilterBackend]
#     # filterset_fields = ['name']
#     filterset_class = TimeFilterSet
    # search_fields = ['interfaces__id']
    # ordering_fields = ['interfaces__id']
    # pagination_class = PageNumberPagination

    # def get_object(self, pk):
    #     try:
    #         obj = Projects.objects.get(id=pk)
    #         return obj
    #     except Exception:
    #         raise Http404

    # def get(self, request, *args, **kwargs):
    #     #获取所有的项目数据
    #     # data = {
    #     #     'name': 'mkmk',
    #     #     'age': 18
    #     # }
    #     # obj = json.dumps(data, ensure_ascii=False)
    #     # qs = Projects.objects.exclude(name="接口测试平台项目")
    #     # qs = Projects.objects.filter(Q(name__contains='测试') | Q(name__endswith='1'))
    #     # tt = []
    #     # for obj in qs:
    #     #     tt.append({
    #     #         'name':obj.name,
    #     #         'leader': obj.leader,
    #     #         'desc': obj.desc
    #     #     })
    #     # obj = Projects.objects.get(id=1)
    #     # inte = Interfaces.objects.create(project=obj)
    #     # # inte = Interfaces.objects.create(project_id=obj.id)
    #     # inte.name = '接口项目1'
    #     # inte.tester = '接口测试负责人A'
    #     # inte.save()
    #     # ob = {
    #     #         'name': inte.name,
    #     #         'leader': inte.tester,
    #     #         'project_id': inte.project_id
    #     #     }
    #     # return JsonResponse(ob, json_dumps_params={'ensure_ascii': False})
    #     # objs = Projects.objects.all()
    #     # objs = self.queryset
    #     # objs = self.get_queryset()
    #     # qs = self.filter_queryset(objs)
    #     # page = self.paginate_queryset(qs)
        # if page is not None:
    #     #     serializer_obj = self.get_serializer(instance=page, many=True)
    #     #     return self.get_paginated_response(serializer_obj.data)
    #     # serializer = self.get_serializer(instance=qs, many=True)
    #     # serializer = ProjectSerializers(instance=objs, many=True)
    #     # obj = []
    #     # for i in objs:
    #     #     obj.append({
    #     #         'id': i.id,
    #     #         'name': i.name,
    #     #         'leader': i.leader
    #     #     })
    #     # return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})
    #     # return Response(serializer.data, status=status.HTTP_200_OK)
    #     return self.list(request, *args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     #创建项目数据
    #     # obj = Projects(name='接口测试平台项目', leader='项目负责人', desc='非常好用的测试平台')
    #     # obj.save()
    #     # obj = Projects.objects.create(name='接口测试平台项目11', leader='项目负责人', desc='非常好用的测试平台')
    #     # objs = {
    #     #     "name": obj.name,
    #     #     "leader": obj.leader,
    #     #     'desc': obj.desc
    #     # }
    #     # obj = Projects.objects.filter(name='接口测试平项目负责人12B', desc='非常好用的测试台项目11', leader='平台')
    #     # obj = Projects.objects.get(id=1)
    #     # st = obj.interfaces_set.all()
    #     # st = Interfaces.objects.filter(project__id=1)
    #     # list = []
    #     # for i in st:
    #     #     list.append({
    #     #         "name": i.name,
    #     #         "leader": i.tester
    #     #     })
    #     # obj = Interfaces.objects.get(id=1)
    #     # objs = {
    #     #     'name': obj.project.name,
    #     #     'leader': obj.project.leader,
    #     #     'desc': obj.project.desc
    #     # }
    #     # objs = Projects.objects.filter(interfaces__id=1)
    #     # list = []
    #     # for i in objs:
    #     #     list.append({
    #     #         "name": i.name,
    #     #         "leader": i.leader,
    #     #         'desc': i.desc
    #     #     })
    #     # obj = Projects.objects.all()
    #     # objs = []
    #     # for i in obj:
    #     #     objs.append({'name': i.name, 'leader': i.leader})
    #     # # 过滤批量更新
    #     # obj = Projects.objects.filter(leader='项目负责人')
    #     # objs = []
    #     # for i in obj:
    #     #     i.leader = "项目负责人B"
    #     #     i.save(update_fields=['leader'])
    #     #     objs.append({'name': i.name, 'leader': i.leader})
    #     # return JsonResponse(objs, safe=False, json_dumps_params={'ensure_ascii': False})
    #     # 更新一条数据
    #     # obj = Projects.objects.get(id=1)
    #     # obj.leader = "项目负责人K"
    #     # obj.save()
    #     # objs = {'name': obj.name, 'leader': obj.leader}
    #     # # 全表数据更新
    #     # Projects.objects.update(leader='项目负责人C')
    #     # # 过滤批量更新
    #     # Projects.objects.filter(leader='').update(leader='')
    #     # Projects.objects.get(id=3).delete()                             #删除一条数据
    #     # Projects.objects.filter(name__startswith='接口测试').delete()       #删除多条数据
    #     # return JsonResponse(objs, json_dumps_params={'ensure_ascii': False})
    #     # # data = {
    #     # #     'name': 'mkmk',
    #     # #     'age': 18
    #     # # }
    #     # # tt = request.body.decode('utf-8')
    #     # # obj = json.loads(tt, encoding='utf-8')
    #     # # # obj = json.dumps(data, ensure_ascii=False)
    #     # # # return HttpResponse(obj)
    #     # return JsonResponse(None)
    #     # return JsonResponse(data, json_dumps_params={'ensure_ascii': False})
    #     # obj = Projects.objects.filter(id__gte=1).order_by('-id')
    #     # # obj = Projects.objects.filter(id__gte=1)
    #     # objs = []
    #     # for i in obj:
    #     #     objs.append({'id': i.id, 'name': i.name, 'leader': i.leader})
    #     # return JsonResponse(objs, safe=False, json_dumps_params={'ensure_ascii': False})
    #     # objs = Projects.objects.filter(id__gt=1).values('id', 'name')
    #     # objs = Projects.objects.filter(id__gt=1).only('id')
    #     # objs = Projects.objects.filter(id__gt=1)
    #     # objs = Projects.objects.filter(id__gt=1).defer('create_time', 'update_time')
    #     # objs = Projects.objects.filter(id__gt=1).values()
    #     # objs = Projects.objects.filter(id__gt=1).values_list('id')
    #     # objs = Projects.objects.values_list('id', flat=True)
    #     # objs = Projects.objects.values('leader').order_by('leader').distinct()
    #     # objs = Projects.objects.values('leader')
    #     # inte = Interfaces.objects.values('id').order_by('id')
    #     # objs = Interfaces.objects.filter(id=1).select_related('project')
    #     # objs = Projects.objects.filter(id=1).select_related('interfaces')
    #     # objs = Interfaces.objects.select_related('project').filter(id=1)
    #     # objs = Interfaces.objects.all().select_related('project')
    #     # objs = Interfaces.objects.select_related('project').get(id=1)
    #     # objs = Interfaces.objects.select_related('project').get(id=1)
    #     # objs = Interfaces.objects.prefetch_related(Prefetch('project', queryset=, to_attr=).get(id=1)
    #     # objs = Interfaces.objects.values('id').annotate(Count('project'))
    #     # objs = Projects.objects.values('id').annotate(Count('interfaces')).order_by('id')
    #     # objs = Projects.objects.filter(id__gte=1)
    #     # for i in objs:
    #     #     ee = i.interfaces_set.all() or i.name
    #     # # obj = Projects.objects.values('leader')
    #     # # qset = objs.union(obj)
    #     # obj = []
    #     # msg = {
    #     #     'msg': "参数异常",
    #     #     'code': 0
    #     # }
    #     # data = request.body.decode(encoding='utf-8')
    #     # try:
    #     #     request_data = json.loads(data)
    #     # except:
    #     #     return JsonResponse(msg, json_dumps_params={'ensure_ascii': False})
    #     # serializer_obj = ProjectSerializers(data=request_data)
    #     # serializer_obj = self.get_serializer(data=request.data)
    #     # serializer_obj.is_valid(raise_exception=True)
    #     # serializer_obj.save()
    #     # # objs = Projects.objects.create(**serializer_obj.validated_data)
    #     # # obj = {
    #     # #     'name': objs.name,
    #     # #     'leader': objs.leader
    #     # # }
    #     # # serializer = ProjectSerializers(instance=objs)
    #     # return Response(serializer_obj.data)
    #     return self.create(request, *args, **kwargs)

    # def put(self, request, id):
    #     msg = {
    #         'msg': "参数异常",
    #         'code': 0
    #     }
    #     # obj = Projects.objects.get(id=id)
    #     obj = self.get_object(id)
    #     data = request.body.decode(encoding='utf-8')
    #     try:
    #         request_data = json.loads(data)
    #     except Exception:
    #         return JsonResponse(msg, json_dumps_params={'ensure_ascii': False})
    #     obj.name = request_data.get('name')
    #     obj.leader = request_data.get('leader')
    #     obj.save(update_fields=['name', 'leader'])
    #     # objs = {
    #     #     'id': obj.id,
    #     #     'name': obj.name,
    #     #     'leader': obj.leader
    #     # }
    #     serializer_obj = ProjectSerializers(instance=obj)
    #     return JsonResponse(serializer_obj.data, json_dumps_params={'ensure_ascii': False})

    # def delete(self, request, id):
    #     # obj = Projects.objects.get(id=id)
    #     obj = self.get_object(id)
    #     obj.delete()
    #     return JsonResponse(None, safe=False, json_dumps_params={'ensure_ascii': False})

    # def patch(self, request):
    #     return HttpResponse()


# class ProjectGetView(mixins.RetrieveModelMixin,
#                      mixins.DestroyModelMixin,
#                      mixins.UpdateModelMixin,
#                      GenericAPIView):
# class ProjectGetView(generics.RetrieveAPIView,
#                      generics.DestroyAPIView,
#                      generics.UpdateAPIView):
# class ProjectGetView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Projects.objects.all()
#     serializer_class = ProjectModelSerializer
#     lookup_field = 'id'
#     # search_fields = ['name']
#     # def get_object(self, pk):
#     #     try:
#     #         obj = Projects.objects.get(id=pk)
#     #         return obj
#     #     except Exception:
#     #         raise Http404
#
#     # def get(self, request, *args, **kwargs):
#     #     #获取所有的项目数(sel据
#     #     # data = {
#     #     #     'name': 'mkmk',
#     #     #     'age': 18
#     #     # }
#     #     # obj = json.dumps(data, ensure_ascii=False)
#     #     # qs = Projects.objects.exclude(name="接口测试平台项目")
#     #     # qs = Projects.objects.filter(Q(name__contains='测试') | Q(name__endswith='1'))
#     #     # tt = []
#     #     # for obj in qs:
#     #     #     tt.append({
#     #     #         'name':obj.name,
#     #     #         'leader': obj.leader,
#     #     #         'desc': obj.desc
#     #     #     })
#     #     # obj = Projects.objects.get(id=1)
#     #     # inte = Interfaces.objects.create(project=obj)
#     #     # # inte = Interfaces.objects.create(project_id=obj.id)
#     #     # inte.name = '接口项目1'
#     #     # inte.tester = '接口测试负责人A'
#     #     # inte.save()
#     #     # ob = {
#     #     #         'name': inte.name,
#     #     #         'leader': inte.tester,
#     #     #         'project_id': inte.project_id
#     #     #     }
#     #     # return JsonResponse(ob, json_dumps_params={'ensure_ascii': False})
#     #     # obj = Projects.objects.get(id=id)
#     #     # obj = self.get_object()
#     #     # # obj_dict = {
#     #     # #     'id': obj.id,
#     #     # #     'name': obj.name,
#     #     # #     'leader': obj.leader
#     #     # # }
#     #     # # serializer_obj = ProjectSerializers(instance=obj)
#     #     # serializer_obj = self.get_serializer(instance=obj)
#     #     # return Response(serializer_obj.data)
#     #     return self.retrieve(request, *args, **kwargs)
#     #
#     # def delete(self, request, *args, **kwargs):
#     #     # obj = Projects.objects.get(id=id)
#     #     # obj = self.get_object()
#     #     # obj.delete()
#     #     # return Response(None)
#     #     return self.destroy(request, *args, **kwargs)
#     #
#     # def put(self, request, *args, **kwargs):
#     #     # msg = {
#     #     #     'msg': "参数异常",
#     #     #     'code': 0
#     #     # }
#     #     # obj = Projects.objects.get(id=id)
#     #     # obj = self.get_object()
#     #     # # data = request.body.decode(encoding='utf-8')
#     #     # # try:
#     #     # #     request_data = json.loads(data)
#     #     # # except Exception:
#     #     # #     return JsonResponse(msg, json_dumps_params={'ensure_ascii': False})
#     #     # # serializer_obj = ProjectSerializers(instance=obj, data=request_data)
#     #     # serializer_obj = self.get_serializer(instance=obj, data=request.data)
#     #     # serializer_obj.is_valid(raise_exception=True)
#     #     # serializer_obj.save()
#     #     # # serializer_obj.save()
#     #     # # obj.name = request_data.get('name')
#     #     # # obj.leader = request_data.get('leader')
#     #     # # obj.save(update_fields=['name', 'leader'])
#     #     # # objs = {
#     #     # #     'id': obj.id,
#     #     # #     'name': obj.name,
#     #     # #     'leader': obj.leader
#     #     # # }
#     #     # # serializer_obj = ProjectSerializers(instance=obj)
#     #     # return Response(serializer_obj.data)
#     #     return self.update(request, *args, **kwargs)
#     # def post(self, request, id):
#     #     obj = Projects.objects.get(id=id)
#     #     data = request.body.decode(encoding='utf-8')
#     #     request_data = json.loads(data)
#     #     obj.name = request_data.get('name')
#     #     obj.leader = request_data.get('leader')
#     #     obj.save(update_fields=['name', 'leader'])
#     #     objs = {
#     #         'id': obj.id,
#     #         'name': obj.name,
#     #         'leader': obj.leader
#     #     }
#     #     return JsonResponse(objs, json_dumps_params={'ensure_ascii': False})
#
#     def patch(self, request, *args, **kwargs):
#         # msg = {
#         #     'msg': "参数异常",
#         #     'code': 0
#         # }
#         # obj = Projects.objects.get(id=id)
#         # obj = self.get_object()
#         # data = request.body.decode(encoding='utf-8')
#         # try:
#         #     request_data = json.loads(data)
#         # except Exception:
#         #     return JsonResponse(msg, json_dumps_params={'ensure_ascii': False})
#         # serializer_obj = ProjectSerializers(instance=obj, data=request_data)
#         serializer_obj = ProjectModelSerializer(instance=self.get_object(), data=request.data, partial=True)
#         serializer_obj.is_valid(raise_exception=True)
#         serializer_obj.save()
#         # serializer_obj.save()
#         # obj.name = request_data.get('name')
#         # obj.leader = request_data.get('leader')
#         # obj.save(update_fields=['name', 'leader'])
#         # objs = {
#         #     'id': obj.id,
#         #     'name': obj.name,
#         #     'leader': obj.leader
#         # }
#         # serializer_obj = ProjectSerializers(instance=obj)
#         return Response(serializer_obj.data)


# class ProjectViewSet(mixins.CreateModelMixin,
#                      mixins.ListModelMixin,
#                      mixins.RetrieveModelMixin,
#                      mixins.UpdateModelMixin,
#                      mixins.DestroyModelMixin,
#                      GenericViewSet):
class ProjectViewSet(ModelViewSet):
    """
    create: 创建项目
    list: 查询所有项目信息
    retrieve: 查询一条项目信息
    update: 全量更新
    partial_update: 部分更新
    destroy: 删除项目信息
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer
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
            testsuites_count = Testsuits.objects.filter(project__id=item.get('id')).count()
            testcases_count = Testcases.objects.filter(interface__project__id=item.get('id')).count()
            interfaces_count = Interfaces.objects.filter(project__id=item.get('id')).count()
            configures_count = Configures.objects.filter(interface__project__id=item.get('id')).count()
            item["interfaces"] = interfaces_count
            item["testcases"] = testcases_count
            item["testsuites"] = testsuites_count
            item["configures"] = configures_count
        return response

    @action(methods=['GET'], detail=False)
    def names(self,request, *args,  **kwargs):
        qs = self.get_queryset()
        serializer_obj = self.get_serializer(instance=qs, many=True)
        return Response(serializer_obj.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def interfaces(self, request, *args, **kwargs):
        qs = self.get_object()
        serializer_obj = self.get_serializer(instance=qs)
        return Response(serializer_obj.data, status=status.HTTP_200_OK)

    # @action(methods=['GET'], detail=False)
    # def selectrelated(self, request, *args, **kwargs):
    #     # qs = Interfaces.objects.prefetch_related(Prefetch('', queryset=, to_attr=''))
    #     # qs = Interfaces.objects.all()
    #     # qs = Interfaces.objects.select_related('project').get(id=1)
    #     qs = Interfaces.objects.get(id=1)
    #     name = qs.name
    #     project_name = qs.project.name
    #     # qs = Interfaces.objects.filter(project__id=1)
    #     # qs = Projects.objects.select_related('interfaces')
    #     return Response(None)

    def get_serializer_class(self):
        if self.action == 'name':
            return ProjectNameModelSerializer
        elif self.action == 'interfaces':
            return ProjectInterfacesSerializer
        else:
            return self.serializer_class

    def paginate_queryset(self, queryset):
        if self.action == 'names':
            return None
        else:
            return super().paginate_queryset(queryset)

    def filter_queryset(self, queryset):
        if self.action == 'names':
            return queryset
        else:
            return super().filter_queryset(queryset)