from rest_framework import serializers
from apps.cart.models import Cart, CartItems,Wishlist,WishlistItem
from apps.product.models import Product


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "name_ar", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    # product = serializers.UUIDField(
    #     required=False, write_only=True
    # )  # Make this field optional
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = [
            "id",
            "cart",
            "product",
            "added_at",
            "quantity",
            "sub_total",
        ]

    def get_sub_total(self, cartitem: CartItems):
        try:
            quantity = int(cartitem.quantity)
            sub_total = quantity * cartitem.product.price
            cartitem.sub_total = sub_total
            return sub_total
        except (ValueError, TypeError):
            return 0  # Handle the case where quantity is not numeric

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep["product"] = SimpleProductSerializer(instance.product).data
    #     return rep


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, required=False)
    grand_total = serializers.SerializerMethodField(method_name="main_total")
    total_quantity = serializers.SerializerMethodField(method_name="total")
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    customer_name = serializers.CharField(source="customer.name", read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "created_at",
            "updated_at",
            "items",
            "customer",
            "customer_name",
            "total_quantity",
            "grand_total",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "items",
        ]

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d")

    def main_total(self, cart: Cart):
        items = cart.items.all()
        grand_total = sum([item.quantity * item.product.price for item in items])
        cart.grand_total = grand_total
        cart.save()
        return grand_total

    def total(self, cart: Cart):
        items = cart.items.all()
        total_quantity = sum([item.quantity for item in items])
        cart.total_quantity = total_quantity
        cart.save()
        return total_quantity

class WishListItemSerializer(serializers.ModelSerializer):
    # product = serializers.UUIDField(
    #     required=False, write_only=True
    # )  # Make this field optional
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = WishlistItem
        fields = [
            "id",
            "wishlist",
            "product",
            "added_at",
            "quantity",
            "sub_total",
        ]

    def get_sub_total(self, wishlistitem: WishlistItem):
        try:
            quantity = int(wishlistitem.quantity)
            sub_total = quantity * wishlistitem.product.price
            wishlistitem.sub_total = sub_total
            return sub_total
        except (ValueError, TypeError):
            return 0  # Handle the case where quantity is not numeric

    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)
    #     rep["product"] = SimpleProductSerializer(instance.product).data
    #     return rep


class WishListSerializer(serializers.ModelSerializer):
    items = WishListItemSerializer(many=True, required=False)
    grand_total = serializers.SerializerMethodField(method_name="main_total")
    total_quantity = serializers.SerializerMethodField(method_name="total")
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    customer_name = serializers.CharField(source="customer.name", read_only=True)

    class Meta:
        model = Wishlist
        fields = [
            "id",
            "created_at",
            "updated_at",
            "items",
            "customer",
            "customer_name",
            "total_quantity",
            "grand_total",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "items",
        ]

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d")

    def main_total(self, wishlist: Wishlist):
        items = wishlist.items.all()
        grand_total = sum([item.quantity * item.product.price for item in items])
        wishlist.grand_total = grand_total
        wishlist.save()
        return grand_total

    def total(self, wishlist: Wishlist):
        items = wishlist.items.all()
        total_quantity = sum([item.quantity for item in items])
        wishlist.total_quantity = total_quantity
        wishlist.save()
        return total_quantity

