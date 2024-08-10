from decimal import Decimal
from django.conf import settings
from product.serializers import ProductSerializer
from product.models import Product
from order.models import Coupon , OrderItem
from typing import Dict, List, Iterator, Optional, Union , Any


class Cart:
    def __init__(self, request):
        """
        initialize the cart
        """
        self.session = request.session
        self.cart: Dict[str, Dict[str, Union[str, int]]] = self.session.get(settings.CART_SESSION_ID, {})
        self.coupon_id = self.session.get('coupon_id')
        self.session[settings.CART_SESSION_ID] = self.cart


    def add(self, product: Product, quantity: int=1, override_quantity: bool = False) -> None:
        """
        Add product to the cart or update its quantity
        """

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price)
            }
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product: Product) -> None:
        """
        Remove a product from the cart
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self) -> Iterator[Dict[str, Union[Decimal, int, Dict[str, Any]]]]:
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_item = self.cart[str(product.id)]
            cart_item["product"] = ProductSerializer(product).data
            cart_item["price"] = Decimal(cart_item["price"])
            cart_item["total_price"] = cart_item["price"] * cart_item["quantity"]
            yield cart_item

    def __len__(self) -> int:
        """
        Count all items in the cart
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_subtotal(self):
        """
        Calculate the subtotal of the cart
        """
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def get_tax(self, tax_rate: Decimal = Decimal(0.1)) -> Decimal:
        """
        Calculate the tax amount based on the subtotal and tax rate.
        """
        subtotal = self.get_subtotal()
        return subtotal * tax_rate / 100

    def get_total_price(self, tax_rate: Decimal) -> Decimal:
        """
        Calculate the total price of the cart.
        """
        subtotal = self.get_subtotal()
        tax = self.get_tax(tax_rate)
        discount = self.get_discount()
        return subtotal + tax - discount
    
    def get_items(self) -> List[OrderItem]:
        """
        Get cart items as a list of OrderItem objects.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        items = []
        for product in products:
            items.append(OrderItem(
                product=product,
                price=Decimal(self.cart[str(product.id)]['price']),
                quantity=self.cart[str(product.id)]['quantity']
            ))
        return items

    
    def apply_coupon(self, coupon_id: int) -> None:
        self.session['coupon_id'] = coupon_id
        self.coupon_id = coupon_id
        self.save()


    @property
    def coupon(self) -> Optional[Coupon]:
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                return None
        return None

    def get_discount(self) -> Decimal:
        """
        Calculate the discount amount.
        """
        return (self.coupon.discount / 100) * self.get_subtotal() if self.coupon else Decimal(0)

    def save(self):
        # Mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def clear(self) -> None:
        """
        Remove cart from session.
        """
        self.session.pop(settings.CART_SESSION_ID, None)
        self.session.pop('coupon_id', None)
        self.save()
