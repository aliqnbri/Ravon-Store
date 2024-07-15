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

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'required': True},
            'category': {'required': True},
            'price': {'required': True},
            'description': {'required': True},
            'image': {'required': True}
            }
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'        

        
