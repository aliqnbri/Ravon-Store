from django.shortcuts import render
from rest_framework import generics , mixins
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
