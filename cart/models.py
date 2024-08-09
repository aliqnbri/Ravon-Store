



from decimal import Decimal

from django.conf import settings

from product.serializers import ProductSerializer
from product.models import Product 
from order.models import Coupon


class Cart:
    def __init__(self, request):
        """
        initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self, product, quantity=1, overide_quantity=False):
        """
        Add product to the cart or update its quantity
        """

        product_id = str(product["id"])
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product["price"])
            }
        if overide_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart
        """
        product_id = str(product["id"])

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()

        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = ProductSerializer(product).data
        for item in cart.values():
            item["price"] = Decimal(item["price"]) 
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item["quantity"] for item in self.cart.values())
    
    def get_subtotal(self):
        """
        Calculate the subtotal of the cart
        """
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())
    
    def get_tax(self, tax_rate):
        """
        Calculate the tax amount based on the subtotal and tax rate
        """
        subtotal = self.get_subtotal()
        return subtotal * (tax_rate / 100)

    def get_total_price(self, tax_rate):
        """
        Calculate the total price of the cart
        """
        subtotal = self.get_subtotal()
        tax = self.get_tax(tax_rate)
        discount = self.get_discount()
        return subtotal + tax - discount
    
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        """
        Calculate the discount amount
        """
        if self.coupon:
            return (self.coupon.discount / 100) * self.get_subtotal()
        return 0

    
    def save(self):
        # Mark the session as "modified" to make sure it gets saved
        self.session.modified = True


    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()