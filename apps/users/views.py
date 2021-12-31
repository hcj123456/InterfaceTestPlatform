from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render
from requests import Response
from rest_framework.decorators import action

from .models import Users
from users.serializers import UserModelSerializer

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.versioning import URLPathVersioning, QueryParameterVersioning, AcceptHeaderVersioning, NamespaceVersioning


class UserViews(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserModelSerializer
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    versioning_class = QueryParameterVersioning

    @action(methods=['GET'], detail=False)
    def check_email(self, request, email):
        # count = self.get_queryset(email).count()
        count = Users.objects.filter(email=email).count()
        data = {
            'count': count,
            'email': email
        }
        return JsonResponse(data)

    def get_queryset(self, *args, **kwargs):

        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )

        queryset = self.queryset
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            if self.action == 'check_email':
                queryset = queryset.filter(email=args[0])
            else:
                queryset = queryset.all()
        return queryset

