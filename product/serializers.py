from rest_framework import serializers
from product.models import Category, Product, Review ,Brand

from django.utils.text import slugify
from rest_framework.reverse import reverse_lazy
from typing import Dict, Any




class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']
        read_only_fields = ['id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id', 'slug']


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
    detail_url = serializers.SerializerMethodField(read_only=True)
    brand = BrandSerializer()

    # category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['id', 'slug']
        extra_kwargs = {
            'name': {'required': True},
            'category': {'required': True},
            'price': {'required': True},
            'description': {'required': True},
            'image': {'required': True}
        }

    def get_detail_url(self, obj: Product) -> str:
        """Returns the detail URL for the product."""
        request = self.context.get('request')
        return request.build_absolute_uri(reverse_lazy("product:products-detail", kwargs={"slug": obj.slug}))

    def create(self, validated_data: Dict[str, Any]) -> Product:
        """Creates a new product instance."""
        categories_data = validated_data.pop('category')
        reviews_data = validated_data.pop('reviews', [])
        product = Product.objects.create(**validated_data)
        product.slug = slugify(product.name)
        product.category.set(categories_data)
        product.reviews.set(reviews_data)
        product.save()
        return product

    def update(self, instance: Product, validated_data: Dict[str, Any]) -> Product:
        """Updates an existing product instance."""
        # Extract category data, default to None
        categories_data = validated_data.pop('category', None)
        # Extract reviews data, default to None
        reviews_data = validated_data.pop('reviews', None)

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
    
    def delete(self, instance):
        instance.delete()


    def to_representation(self, instance: Product) -> Dict[str, Any]:
        """ Returns the representation of the product instance."""


        data = super().to_representation(instance)
        view = self.context.get('view')
        data['detail_url'] = self.get_detail_url(instance)
        data['category'] = [category.name for category in instance.category.all()]

        data['brand'] = instance.brand.name

        match view.action:
            case 'list'| 'filter_by_category':
                excluded_fields = ['created_at', 'updated_at', 'is_active', 'slug', 'description',  'reviews']
                for field in excluded_fields:
                    data.pop(field, None)
            case _:
                data.pop('detail_url', None)        
        return data        

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","name", "price"]   
    


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


