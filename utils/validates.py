from projects.models import Projects
from interfaces.models import Interfaces
from envs.models import Envs
from rest_framework import serializers


def is_project_id_existed(id):
    if not Projects.objects.filter(id=id).exists():
        raise serializers.ValidationError('该项目id不存在')


def is_interface_id_existed(id):
    if not Interfaces.objects.filter(id=id).exists():
        raise serializers.ValidationError('该接口id不存在')


def is_env_id_existed(id):
    if not Envs.objects.filter(id=id).exists():
        raise serializers.ValidationError('该环境id不存在')
