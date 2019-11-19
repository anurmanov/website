from rest_framework import serializers
from goods.models import Category

class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(max_length = 200)
    class Meta:
        model = Category
        fields = ['name', 'parent_name']

