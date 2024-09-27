from rest_framework import serializers
from .models import News, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class NewsSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = News
        fields = ['id', 'title', 'summary',
                  'source_url', 'source_name', 'published_at', 'updated_at', 'category', 'og_image_url']
