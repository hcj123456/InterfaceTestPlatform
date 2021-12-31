from rest_framework import serializers
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from .models import Users


class UserModelSerializer(serializers.ModelSerializer):
    # password_confirm = serializers.CharField(max_length=20, min_length=6, write_only=True)
    # token = serializers.CharField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['token'] = serializers.CharField(read_only=True)
        self.fields['password_confirm'] = serializers.CharField(max_length=20, min_length=6, write_only=True)

    class Meta:
        model = Users
        # fields = ('id', 'username', 'password', 'email', 'password_confirm', 'token')
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {
            'username': {
                'max_length': 20,
                'min_length': 6
            },
            'password': {
                'max_length': 20,
                'min_length': 6
            },
            'email': {
                'required': True,
                'error_messages': {
                    'required': '邮箱不能为空'
                }
            }
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError("密码和确认密码不一致")
        return attrs

    # def to_internal_value(self, data):
    #     obj_data = super().to_internal_value(data)
    #     obj_data.pop('password_confirm')
    #     obj = Users.objects.create_user(**obj_data)
    #     return obj
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        obj = Users.objects.create_user(**validated_data)
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        obj.token = token
        return obj



