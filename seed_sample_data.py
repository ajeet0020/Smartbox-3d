import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from shipping.models import Product, Box, Order, OrderItem

def seed():
    # Clear existing sample records
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    Box.objects.all().delete()

    # Create Boxes
    small = Box.objects.create(
        name="Small Box",
        inner_length=20,
        inner_width=15,
        inner_height=15,
        max_weight=5,
        cost=20.00,
        is_active=True
    )
    medium = Box.objects.create(
        name="Medium Box",
        inner_length=30,
        inner_width=25,
        inner_height=20,
        max_weight=10,
        cost=35.00,
        is_active=True
    )
    large = Box.objects.create(
        name="Large Box",
        inner_length=45,
        inner_width=35,
        inner_height=30,
        max_weight=20,
        cost=60.00,
        is_active=True
    )

    # Create Products
    mug = Product.objects.create(
        name="Coffee Mug",
        sku="MUG-001",
        length=10,
        width=10,
        height=12,
        weight=0.400
    )
    book = Product.objects.create(
        name="Hardcover Book",
        sku="BK-001",
        length=25,
        width=18,
        height=3,
        weight=0.800
    )
    shoes = Product.objects.create(
        name="Running Shoes",
        sku="SH-001",
        length=32,
        width=20,
        height=12,
        weight=1.100
    )

    # Create a Sample Order
    order = Order.objects.create(reference="ORD-2026-001")
    OrderItem.objects.create(order=order, product=mug, quantity=2)
    OrderItem.objects.create(order=order, product=book, quantity=1)

    print("Sample data populated successfully!")
    print(f"Boxes created: {Box.objects.count()} (Small, Medium, Large)")
    print(f"Products created: {Product.objects.count()} (Mug [id={mug.id}], Book [id={book.id}], Shoes [id={shoes.id}])")
    print(f"Order created: {order.reference} [id={order.id}]")

if __name__ == "__main__":
    seed()

