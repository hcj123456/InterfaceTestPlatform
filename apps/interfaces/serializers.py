from rest_framework import serializers

from projects.models import Projects
from .models import Interfaces
from configures.models import Configures
from testcases.models import Testcases


class InterfaceModelSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(label='项目名称', help_text='项目名称', max_length=10, min_length=5,
    #                              validators=[UniqueValidator(Projects.objects.all(), message="该字段不允许为空"),
    #                                          is_contains],
    #                              error_messages={'min_length': '请保证该字段值大于等于5个字符',
    #                                              'max_length': '请保证这个字段只能小于等于8个字符'})
    # leader = serializers.CharField(label='项目负责人', help_text='项目负责人', max_length=20, min_length=2)
    # email = serializers.EmailField(write_only=True)
    # project = serializers.PrimaryKeyRelatedField(read_only=True)
    # project = serializers.StringRelatedField(label='', help_text='')
    # project = serializers.SlugRelatedField(slug_field='leader', read_only=True)
    project = serializers.StringRelatedField(label='项目名称', help_text='项目名称')
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), label='项目id', help_text='项目id')

    class Meta:
        model = Interfaces
        # fields = '__all__'
        # fields = ('id', 'name', 'leader', 'email')
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }

    # def create(self, validated_data):
    #     project_id = validated_data.pop('project')
    #     validated_data['project_id'] = project_id.id
    #     obj = Interfaces.objects.create(**validated_data)
    #     return obj
    def to_internal_value(self, data):
        obj = super().to_internal_value(data)
        project = obj.pop('project_id')
        project: Projects
        obj['project'] = project
        return obj

    def to_representation(self, instance):
        obj = super().to_representation(instance)
        obj.pop('project_id')
        return obj


class ConfiguresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configures
        fields = ('id', 'name')


class ConfiguresByInterfacesIdSerializer(serializers.ModelSerializer):

    configures = ConfiguresSerializer(read_only=True, many=True)

    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'configures')


class TestcasesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Testcases
        fields = ('id', 'name')


class TestcasesByInterfacesIdSerializer(serializers.ModelSerializer):

    testcases = TestcasesSerializer(read_only=True, many=True)

    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'testcases')