from rest_framework import serializers

from .models import Box, Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "sku", "length", "width", "height", "weight"]


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ["id", "name", "inner_length", "inner_width", "inner_height",
                  "max_weight", "cost", "is_active"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("quantity must be at least 1")
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "reference", "created_at", "items"]
        read_only_fields = ["created_at"]

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("an order needs at least one item")
        return value

    def create(self, validated_data):
        items = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        OrderItem.objects.bulk_create(OrderItem(order=order, **i) for i in items)
        return order


class RecommendLineSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class RecommendRequestSerializer(serializers.Serializer):
    items = RecommendLineSerializer(many=True, allow_empty=False)

    def validate_items(self, value):
        ids = {i["product_id"] for i in value}
        found = set(Product.objects.filter(id__in=ids).values_list("id", flat=True))
        missing = sorted(ids - found)
        if missing:
            raise serializers.ValidationError(f"unknown product ids: {missing}")
        return value
