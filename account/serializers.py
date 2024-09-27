from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser
from news.models import Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'date_joined']
        # 'is_staff', 'is_active', 'is_superuser', 'last_login', 'groups', 'user_permissions'


class CustomUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CustomUser
        fields = ['user', 'google_id', 'picture', 'likes', 'dislikes']
        depth = 1


class CreatePreferenceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    likes = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()))
    dislikes = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()))

    class Meta:
        model = CustomUser
        fields = ['user', 'likes', 'dislikes']
