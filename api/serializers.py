from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Checkbox


class CheckboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checkbox
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'