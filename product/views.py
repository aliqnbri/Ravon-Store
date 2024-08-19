from rest_framework import viewsets, permissions ,status
from product.models import Product , Category ,Review
from product.serializers import ProductSerializer , CategorySerializer
from rest_framework.response import Response
from django.utils.text import slugify
from rest_framework.decorators import action
from account.authentications import CustomJWTAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django.views.generic import TemplateView


class ProductTemplateView(TemplateView):
    template_name = 'product/product-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(is_available=True).order_by('-created_at')
        context['products'] = products
        return context

class ProductDetailTemplateView(TemplateView):
    template_name = 'product/product_details.html'




class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """
    serializer_class = ProductSerializer
    authentication_classes = [CustomJWTAuthentication,]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name','category__name', 'brand__name']
    ordering_fields = ['name','created_at', 'price']
    permission_classes = [permissions.AllowAny,]
    lookup_field = 'slug'

    def get_queryset(self):
        """Queryset to include only available Products"""
        return Product.objects.filter(is_available=True).order_by('-created_at')
    

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single category by slug"""
        product = self.get_object()
        serializer = self.get_serializer(product,context={'request': request, 'view': self})
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, slug=None):
        """Delete a category"""
        product = self.get_object()
        serializer = self.get_serializer(product)
        serializer.delete(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], url_path='category/(?P<category_slug>[^/.]+)')
    def filter_by_category(self, request, category_slug=None,):
    
        products = self.get_queryset().filter(category__slug=category_slug)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




