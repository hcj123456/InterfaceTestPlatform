from rest_framework import serializers

from projects.models import Projects
from .models import Configures
from configures.models import Configures
from testcases.models import Testcases
from interfaces.models import Interfaces
from utils.validates import is_project_id_existed, is_env_id_existed, is_interface_id_existed


class InterfaceProjectSerializer(serializers.ModelSerializer):
    iid = serializers.IntegerField(write_only=True, label='接口id', help_text='接口id', validators=[is_interface_id_existed])
    pid = serializers.IntegerField(write_only=True, label='项目id', help_text='项目id', validators=[is_project_id_existed])
    project = serializers.StringRelatedField(label='项目名称', help_text='项目名称')

    class Meta:
        model = Interfaces
        fields = ('iid', 'name', 'pid', 'project')
        extra_kwargs = {
            'name': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        if not Interfaces.objects.filter(id=attrs.get('iid'), project_id=attrs.get('pid')).exists():
            raise serializers.ValidationError('项目id与接口id不一致')
        return attrs


class ConfigureModelSerializer(serializers.ModelSerializer):

    interface = InterfaceProjectSerializer(help_text='项目id和接口id')

    class Meta:
        model = Configures
        fields = ('id', 'name', 'interface', 'author', 'request')
        extra_kwargs = {
            'request': {
                'write_only': True
            }
        }

    def to_internal_value(self, data):
        obj = super().to_internal_value(data)
        inter = obj.pop('interface')
        obj['interface_id'] = inter.get('iid')
        return obj



