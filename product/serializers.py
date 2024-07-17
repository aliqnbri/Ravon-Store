from rest_framework import serializers
from product.models import Category , Product , Review
from rest_framework.reverse import reverse
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'required': True}
            }

class ProductSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
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
        
    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("product-detail", kwargs={"slug": obj.slug}, request=request)

        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'        

        
