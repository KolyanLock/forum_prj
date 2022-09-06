from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Checkbox


class CheckboxSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Checkbox
        fields = ['title', 'is_checked']

    @staticmethod
    def get_title(obj):
        return obj.name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class DataSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    attrs = serializers.JSONField(required=False)
    type = serializers.CharField(required=False)
    val_1 = serializers.IntegerField()
    val_2 = serializers.IntegerField()

    @staticmethod
    def validate_type(type):
        if type not in ['dict', 'list', 'tuple']:
            raise serializers.ValidationError(f'{type} is not allowed')
        return type
