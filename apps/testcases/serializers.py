from rest_framework import serializers
from testcases.models import Testcases
from interfaces.models import Interfaces
from utils.validates import is_interface_id_existed, is_project_id_existed, is_env_id_existed


class InterfaceProjectName(serializers.ModelSerializer):

    pid = serializers.IntegerField(label='项目id', help_text='项目id', write_only=True, validators=[is_project_id_existed])
    project = serializers.StringRelatedField(label='项目名称', help_text='项目名称')
    iid = serializers.IntegerField(label='接口id', help_text='接口id', write_only=True, validators=[is_interface_id_existed])

    class Meta:
        model = Interfaces
        fields = ('name', 'project', 'pid', 'iid')
        extra_kwargs = {
            'name': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        if not Interfaces.objects.filter(id=attrs.get('iid'), project_id=attrs.get('pid')).exists():
            raise serializers.ValidationError("项目id和接口id不一致")
        return attrs


class TestcaseModelSerializer(serializers.ModelSerializer):
    interface = InterfaceProjectName(label='接口和项目', help_text='接口和项目')

    class Meta:
        model = Testcases
        fields = ('id', 'name', 'author', 'interface', 'include', 'request')
        extra_kwargs = {
            'include': {
                'write_only': True
            },
            'request': {
                'write_only': True
            }
        }

    def to_internal_value(self, data):
        response = super().to_internal_value(data)
        ter = response.pop('interface')
        response['interface_id'] = ter.get('iid')
        return response