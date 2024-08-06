from rest_framework import serializers
from product.models import Category , Product , Review
from rest_framework.reverse import reverse
from django.utils.text import slugify

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'name': {'required': True}
            }
        
    def create(self, validated_data):
        category = Category(**validated_data)
        category.slug = slugify(category.name)
        category.save()
        return category

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            instance.slug = slugify(validated_data['name'])
        return super().update(instance, validated_data)    

class ProductSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id','slug']
        extra_kwargs = {
            'name': {'required': True},
            'category': {'required': True},
            'price': {'required': True},
            'description': {'required': True},
            'image': {'required': True}
            }
        
    def get_url(self, obj):
        request = self.context.get('request')
        return reverse("product:product_detail", kwargs={"slug": obj.slug}, request=request)
    
    def create(self, validated_data):
        categories_data = validated_data.pop('category')  
        reviews_data = validated_data.pop('reviews', [])  
        product = Product.objects.create(**validated_data)  
        product.slug = slugify(product.name)
        product.category.set(categories_data)  
        product.reviews.set(reviews_data)  
        product.save()
        return product

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('category', None)  # Extract category data, default to None
        reviews_data = validated_data.pop('reviews', None)  # Extract reviews data, default to None

        if 'name' in validated_data:
            instance.slug = slugify(validated_data['name'])

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update ManyToMany fields if provided
        if categories_data is not None:
            instance.category.set(categories_data)
        if reviews_data is not None:
            instance.reviews.set(reviews_data)

        instance.save()
        return instance

        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'        



class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","name", "price"]   
        
