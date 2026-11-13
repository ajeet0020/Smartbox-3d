from rest_framework.test import APITestCase

from shipping.models import Box, Order, Product


class ApiTests(APITestCase):
    def setUp(self):
        self.mug = Product.objects.create(name="Mug", sku="MUG", length=10, width=10, height=12, weight="0.4")
        self.book = Product.objects.create(name="Book", sku="BK", length=25, width=18, height=3, weight="0.8")
        self.small = Box.objects.create(name="Small", inner_length=20, inner_width=15, inner_height=15,
                                        max_weight=5, cost="20")
        self.large = Box.objects.create(name="Large", inner_length=40, inner_width=30, inner_height=30,
                                        max_weight=20, cost="45")

    def post(self, items):
        return self.client.post("/api/recommend-box/", {"items": items}, format="json")

    def test_recommend_small_box_for_mug(self):
        r = self.post([{"product_id": self.mug.id, "quantity": 1}])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["status"], "ok")
        self.assertEqual(r.data["recommended_box"]["name"], "Small")

    def test_larger_order_needs_large_box(self):
        r = self.post([{"product_id": self.book.id, "quantity": 2}, {"product_id": self.mug.id, "quantity": 2}])
        self.assertEqual(r.data["recommended_box"]["name"], "Large")

    def test_inactive_box_ignored(self):
        self.small.is_active = False
        self.small.save()
        r = self.post([{"product_id": self.mug.id, "quantity": 1}])
        self.assertEqual(r.data["recommended_box"]["name"], "Large")

    def test_duplicate_lines_are_merged(self):
        r = self.post([{"product_id": self.mug.id, "quantity": 1}, {"product_id": self.mug.id, "quantity": 2}])
        self.assertEqual(r.data["total_units"], 3)

    def test_no_box_fits_response(self):
        r = self.post([{"product_id": self.book.id, "quantity": 30}])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["status"], "no_box_fits")

    def test_quantity_zero_is_400(self):
        self.assertEqual(self.post([{"product_id": self.mug.id, "quantity": 0}]).status_code, 400)

    def test_empty_items_is_400(self):
        self.assertEqual(self.post([]).status_code, 400)

    def test_unknown_product_is_400(self):
        self.assertEqual(self.post([{"product_id": 9999, "quantity": 1}]).status_code, 400)

    def test_negative_dimension_rejected_on_create(self):
        r = self.client.post("/api/products/", {"name": "X", "sku": "X", "length": -1, "width": 1,
                                                "height": 1, "weight": 1}, format="json")
        self.assertEqual(r.status_code, 400)

    def test_saved_order_recommendation(self):
        r = self.client.post("/api/orders/", {"reference": "ORD-1", "items": [
            {"product": self.mug.id, "quantity": 1}]}, format="json")
        self.assertEqual(r.status_code, 201)
        r = self.client.get(f"/api/orders/{Order.objects.get().id}/recommend-box/")
        self.assertEqual(r.data["recommended_box"]["name"], "Small")
