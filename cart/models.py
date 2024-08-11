from decimal import Decimal
from django.conf import settings
from product.serializers import ProductSerializer
from product.models import Product
from order.models import Coupon, OrderItem
from typing import Dict, List, Iterator, Optional, Union, Any


class Cart:
    def __init__(self, request):
        """
        initialize the cart
        """
        self.session = request.session
        self.cart: Dict[str, Dict[str, Union[str, int]]
                        ] = self.session.get(settings.CART_SESSION_ID, {})
        self.coupon_id = self.session.get('coupon_id')
        self.session[settings.CART_SESSION_ID] = self.cart

    def add(self, product: Product, quantity: int = 1, override_quantity: bool = False) -> None:
        """
        Add product to the cart or update its quantity
        """
        product_id = str(product.id)
        cart_item = self.cart.setdefault(
            product_id, {"quantity": 0, "price": str(product.price)})
        cart_item["quantity"] = quantity if override_quantity else cart_item["quantity"] + quantity
        self.save()

    def update(self, old_product: Optional[Product] = None, new_product: Optional[Product] = None, quantity: Optional[int] = None) -> None:

        match (old_product, new_product, quantity):
            # Case 1: Replace old_product with new_product and update quantity
            case old_product, new_product, quantity if old_product and new_product:
                old_product_id, new_product_id = str(
                    old_product.id), str(new_product.id)

            # Remove old product if it's different from new product
                if old_product_id != new_product_id:
                    self.remove(old_product)

                # Add or update new product
                self.cart[new_product_id] = {
                    "quantity": quantity if quantity is not None else self.cart.get(old_product_id, {}).get("quantity", 1),
                    "price": str(new_product.price)
                }

            # Case 2: Update the quantity of old_product
            case old_product, None, quantity if old_product and quantity is not None:
                if (old_product_id := str(old_product.id)) in self.cart:
                    self.cart[old_product_id]["quantity"] = quantity

            # Case 3: Add a new product with specified quantity or default quantity 1
            case None, new_product, quantity if new_product:
                self.add(
                    new_product, quantity if quantity is not None else 1, override_quantity=True)

            # Case 4: Do nothing when no valid inputs are provided
            case _:
                return  # Or handle error

        # Save the cart after updating
        self.save()

    def remove(self, product: Product) -> None:
        """
        Remove a product from the cart
        """
        if (product_id := str(product.id)) in self.cart:
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
            cart_item["total_price"] = cart_item["price"] * \
                cart_item["quantity"]
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

    def get_tax(self, tax_rate: Decimal = Decimal(0.2)) -> Decimal:
        """
        Calculate the tax amount based on the subtotal and tax rate.
        """
        return round((self.get_subtotal()) * tax_rate / 100, 2)

    def get_total_price(self, tax_rate=Decimal(0.2)) -> Decimal:
        """
        Calculate the total price of the cart.
        """
        return (self.get_subtotal()) + (self.get_tax(tax_rate)) - (self.get_discount())

    def get_items(self) -> List[OrderItem]:
        """
        Get cart items as a list of OrderItem objects.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        items = (
            OrderItem(
                product=product,
                price=Decimal(self.cart[str(product.id)]['price']),
                quantity=self.cart[str(product.id)]['quantity']
            )
            for product in products
        )
        return list(items)

    def apply_coupon(self, coupon_id: int) -> None:
        self.session['coupon_id'] = coupon_id
        self.coupon_id = coupon_id
        self.save()

    @property
    def coupon(self) -> Optional[Coupon]:
        return Coupon.objects.filter(id=self.coupon_id).first() if self.coupon_id else None

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
