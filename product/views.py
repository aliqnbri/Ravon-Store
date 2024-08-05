# from django.shortcuts import render , get_object_or_404
# from rest_framework import generics , mixins ,permissions , authentication
# from product.models import Product , Category ,Review
# from product.serializers import ProductSerializer , CategorySerializer
# from rest_framework.response import Response
# from django.utils.text import slugify


# # Create your views here.

# class ProductMixinView(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     generics.GenericAPIView
# ):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = ProductSerializer
#     lookup_field = 'slug'



#     def get_queryset(self):
#         """queryset to include only available Product"""
    
#         # category_slug = self.kwargs.get('category_slug')
#         # return Product.objects.filter(category__slug=category_slug)
#         queryset = Product.objects.filter(available=True).order_by('-created_at')
#         return queryset
    
#     def get_object(self):
#         queryset = self.get_queryset
#         lookup_url_kwarg = self.lookup_field
#         filter_kwargs = {lookup_url_kwarg: self.kwargs[lookup_url_kwarg]}
#         obj = get_object_or_404(queryset, **filter_kwargs)
#         return obj

#     def get(self,request, *args,**kwargs):
#         slug = kwargs.get('slug')
    
#         if slug is not None:
#             return self.retrieve(request, *args, **kwargs)
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
#     def perform_create(self, serializer):
#         return super().perform_create(serializer)
    
#     def destroy(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
    
#     def update(self, request):
#         slug = self.lookup_field
#         instance = self.get_object(Product,slug=slug)
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

#     def perform_update(self, serializer):
#         instance = serializer.save()
#         if instance.name != serializer.validated_data.get('name'):
#             instance.slug = slugify(instance.name)
#             instance.save()
#         return instance
    
# class CategoryMixinView(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.UpdateModelMixin,
#     generics.GenericAPIView
# ):
 
#     serializer_class = CategorySerializer
#     lookup_field = 'slug'

#     def get_queryset(self):
#         """queryset to include only available Category"""
#         queryset = Category.objects.filter(available=True).order_by('-created_at')
#         return queryset
    

#     def get(self,request, *args,**kwargs):
#         slug = self.kwargs.get('slug')
#         if slug is not None:
#             return self.retrieve(request, *args, **kwargs)
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
#     def destroy(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
    
#     def update(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
       
    

