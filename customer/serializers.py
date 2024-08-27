from rest_framework import serializers
from customer.models import Address, Comment ,CustomerProfile
from customer.models import CustomUser
from product.models import WishListItem


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['customer']

    def validate(self, attrs):
        user = CustomUser.objects.get(username=self.context['request'].user)
        attrs['customer'] = user
        return super().validate(attrs)


class WishListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListItem
        fields = "__all__"



class CustomerProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['customer', 'gender', 'avatar', 'addresses']
        read_only_fields = ['customer']
        depth = 2
