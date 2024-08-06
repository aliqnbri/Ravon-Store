from rest_framework import viewsets, permissions ,status
from product.models import Product , Category ,Review
from product.serializers import ProductSerializer , CategorySerializer
from rest_framework.response import Response
from django.utils.text import slugify
from rest_framework.decorators import action
from account.authentications import CustomJWTAuthentication

class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """
    serializer_class = ProductSerializer
    authentication_classes = [CustomJWTAuthentication,]
    permission_classes = [permissions.AllowAny,]
    lookup_field = 'slug'

    def get_queryset(self):
        """Queryset to include only available Products"""
        return Product.objects.filter(is_available=True).order_by('-created_at')
    
    def list(self, request):
        """List all available categories"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        """Retrieve a single category by slug"""
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)


    def create(self, request):
        """Create a new category"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def update(self, request, slug=None):
        """Update an existing category"""
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='category/(?P<category_slug>[^/.]+)')
    def filter_by_category(self, request, category_slug=None):
        products = self.get_queryset().filter(category__slug=category_slug)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)        


class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomJWTAuthentication,]
    serializer_class = CategorySerializer

    permission_classes = [permissions.AllowAny,]
    lookup_field = 'slug'

    def get_queryset(self):
        """Queryset to include only available Categories"""
        return Category.objects.filter(is_available=True).order_by('-created_at')


