from rest_framework import serializers
from customer.models import Address,WishListItem,Comment
from accounts.models import CustomUser

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','customer','name','country','state','city','address','postal_code']
        read_only_fields = ['customer']
    def validate(self, attrs):
        user = CustomUser.objects.get(username = self.context['request'].user)
        attrs['customer'] = user
        return super().validate(attrs)
        
        
        
class WishListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListItem
        fields = "__all__"