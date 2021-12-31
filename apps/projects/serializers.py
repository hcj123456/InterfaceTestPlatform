from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Projects
from interfaces.models import Interfaces
from debugtalks.models import DebugTalks

# def is_contains(value):
#     if not '项目' in value:
#         raise serializers.ValidationError('请项目名称不包含项目')


# class ProjectSerializers(serializers.Serializer):
#
#     id = serializers.IntegerField(label='项目id', help_text='项目id', read_only=True)
#     name = serializers.CharField(label='项目名称', help_text='项目名称', max_length=8, min_length=5,
#                                  validators=[UniqueValidator(Projects.objects.all(), message="该字段不允许为空"), is_contains],
#                                  error_messages={'min_length': '请保证该字段值大于等于5个字符',
#                                                  'max_length': '请保证这个字段只能小于等于8个字符'})
#     leader = serializers.CharField(label='项目负责人', help_text='项目负责人', max_length=20, min_length=2,
#                                    allow_null=True, allow_blank=True, default='赐姓大家负责人', write_only=True)
#     token = serializers.CharField(read_only=True)
#
#     def validate_leader(self, value):
#         if not value.endswith('负责人'):
#             raise serializers.ValidationError('该字段必须以负责人结尾')
#         return value
#
#     def validate(self, attrs):
#         name = attrs.get('name')
#         leader = attrs.get('leader')
#         if not '项目' in name or not leader.startswith('测试'):
#             raise serializers.ValidationError("不满足要求")
#         return attrs
#
#     def create(self, validated_data):
#         pro = Projects.objects.create(**validated_data)
#         return pro
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name')
#         instance.leader = validated_data.get('leader')
#         instance.save(update_fields=['name', 'leader'])
#         instance.token = 'nknkkkmkkkkggygygg'
#         return instance


class InterfacesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interfaces
        fields = ('id', 'name')


class ProjectModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label='项目名称', help_text='项目名称', max_length=30, min_length=5,
                                 validators=[UniqueValidator(Projects.objects.all(), message="该字段不允许为空")],
                                 error_messages={'min_length': '请保证该字段值大于等于5个字符',
                                                 'max_length': '请保证这个字段只能小于等于8个字符',
                                                 'required': '该字段是必填，不能为空'})
    leader = serializers.CharField(label='项目负责人', help_text='项目负责人', max_length=8, min_length=5)
    desc = serializers.CharField(label='项目描述', help_text='项目描述', allow_null=True, allow_blank=True, default='')
    create_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    # interfaces_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # interfaces_set = serializers.StringRelatedField(many=True)
    # interfaces_set = serializers.SlugRelatedField(slug_field='tester', read_only=True, many=True)
    # interfaces_set = InterfacesNameSerializer(read_only=True, many=True)

    class Meta:
        model = Projects
        # fields = '__all__'
        # fields = ('id', 'name', 'leader', 'desc', 'email')
        exclude = ('update_time',)

    # def validate(self, attrs):
    #     name = attrs.get('name')
    #     leader = attrs.get('leader')
    #     if not '项目' in name:
    #         raise serializers.ValidationError("不满足要求")
    #     attrs.pop('email')
    #     return attrs

    def create(self, validated_data):
        # validated_data.pop('email')
        # pro = Projects.objects.create(**validated_data)
        project = super().create(validated_data)
        DebugTalks.objects.create(project_id=project.id)
        return project

    def update(self, instance, validated_data):
        # validated_data.pop('email')
        # obj = super().update(instance, validated_data)
        # obj.token = ',lmmlmmmml'
        instance: Projects
        instance.programmer = validated_data.get('programmer')
        instance.save(update_fields=['programmer'])
        return instance


class ProjectNameModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ('id', 'name')


class ProjectInterfacesSerializer(serializers.ModelSerializer):

    interfaces = InterfacesSerializer(read_only=True, many=True)

    class Meta:
        model = Projects
        fields = ('id', 'name', 'interfaces')