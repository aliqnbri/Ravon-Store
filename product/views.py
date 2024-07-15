from django.shortcuts import render
from rest_framework import generics , mixins ,permissions , authentication
from product.models import Product , Category ,Review
from product.serializers import ProductSerializer , CategorySerializer

# Create your views here.

class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return super().get_queryset()
    

    def get(self,request, *args,**kwargs):
        slug = self.kwargs.get('slug')
        if slug is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
class CategoryMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView
):
    permission_classes = [permissions.AllowAny]
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        """queryset to include only available products"""
        queryset = Category.objects.filter(available=True).order_by('-created')
        return queryset
    

    def get(self,request, *args,**kwargs):
        slug = self.kwargs.get('slug')
        if slug is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
       
    

