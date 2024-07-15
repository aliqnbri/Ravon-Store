from rest_framework import serializers
from product.models import Category , Product , Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'required': True}
            }
        