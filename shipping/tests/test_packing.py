from decimal import Decimal as D

from django.test import SimpleTestCase

from shipping.services.packing import (MAX_UNITS, BoxSpec, ItemSpec, can_pack,
                                       item_fits_in_box, recommend_box)


def box(id, dims, max_weight, cost, name=None):
    return BoxSpec(id, name or f"B{id}", *dims, max_weight, cost)


def item(dims, weight=1):
    return ItemSpec(*dims, weight)


class ItemFitTests(SimpleTestCase):
    def test_exact_fit(self):
        self.assertTrue(item_fits_in_box((10, 20, 30), (10, 20, 30)))

    def test_fits_only_after_rotation(self):
        self.assertTrue(item_fits_in_box((30, 10, 20), (10, 20, 30)))

    def test_too_big_in_one_dimension(self):
        self.assertFalse(item_fits_in_box((10, 20, 31), (10, 20, 30)))


class PackingTests(SimpleTestCase):
    def test_eight_cubes_fill_cube_box(self):
        self.assertTrue(can_pack([(1, 1, 1)] * 8, (2, 2, 2)))

    def test_nine_cubes_do_not_fit_cube_box(self):
        self.assertFalse(can_pack([(1, 1, 1)] * 9, (2, 2, 2)))

    def test_two_items_that_each_fit_but_not_together(self):
        # volume total 2*6*6*6=432 <= 500 but they cannot share a 5x5x20 box
        self.assertFalse(can_pack([(6, 6, 6)] * 2, (5, 5, 20)))

    def test_mixed_sizes(self):
        self.assertTrue(can_pack([(10, 10, 5), (10, 10, 5), (5, 5, 5)], (10, 10, 15)))


class RecommendTests(SimpleTestCase):
    def test_picks_cheapest_fitting_box(self):
        boxes = [box(1, (30, 30, 30), 20, D("40")), box(2, (20, 20, 20), 20, D("25"))]
        r = recommend_box([(item((10, 10, 10)), 1)], boxes)
        self.assertEqual(r["status"], "ok")
        self.assertEqual(r["recommended"].id, 2)
        self.assertEqual([b.id for b in r["alternatives"]], [1])

    def test_equal_cost_prefers_smaller_volume(self):
        boxes = [box(1, (30, 30, 30), 20, D("25")), box(2, (20, 20, 20), 20, D("25"))]
        r = recommend_box([(item((10, 10, 10)), 1)], boxes)
        self.assertEqual(r["recommended"].id, 2)

    def test_weight_too_high_rejects_box(self):
        boxes = [box(1, (50, 50, 50), 5, D("10")), box(2, (50, 50, 50), 50, D("30"))]
        r = recommend_box([(item((10, 10, 10), weight=6), 1)], boxes)
        self.assertEqual(r["recommended"].id, 2)
        self.assertEqual(r["rejected"][0]["reason"], "exceeds max weight")

    def test_volume_too_high_rejects_box(self):
        r = recommend_box([(item((10, 10, 10)), 2)], [box(1, (10, 10, 15), 100, D("5"))])
        self.assertEqual(r["status"], "no_box_fits")
        self.assertEqual(r["rejected"][0]["reason"], "exceeds box volume")

    def test_no_box_fits(self):
        r = recommend_box([(item((100, 100, 100)), 1)], [box(1, (10, 10, 10), 10, D("5"))])
        self.assertEqual(r["status"], "no_box_fits")

    def test_quantity_expands_units_and_weight(self):
        r = recommend_box([(item((5, 5, 5), weight=2), 3)], [box(1, (20, 20, 20), 100, D("5"))])
        self.assertEqual(r["total_units"], 3)
        self.assertEqual(r["total_weight"], 6)

    def test_too_many_units_guard(self):
        r = recommend_box([(item((1, 1, 1)), MAX_UNITS + 1)], [box(1, (50, 50, 50), 999, D("5"))])
        self.assertEqual(r["status"], "too_many_units")

    def test_empty_order_raises(self):
        with self.assertRaises(ValueError):
            recommend_box([], [box(1, (10, 10, 10), 10, D("5"))])
