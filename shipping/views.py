from collections import defaultdict

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Box, Order, Product
from .serializers import (BoxSerializer, OrderSerializer, ProductSerializer,
                          RecommendRequestSerializer)
from .services.packing import BoxSpec, ItemSpec, recommend_box


def _box_spec(b):
    return BoxSpec(id=b.id, name=b.name, length=b.inner_length, width=b.inner_width,
                   height=b.inner_height, max_weight=b.max_weight, cost=b.cost)


def _box_json(b):
    return {"id": b.id, "name": b.name, "cost": str(b.cost)}


def run_recommendation(lines):
    """lines: iterable of (product_id, quantity). Duplicate products are merged."""
    qty = defaultdict(int)
    for pid, q in lines:
        qty[pid] += q
    products = Product.objects.in_bulk(qty.keys())
    order_lines = [
        (ItemSpec(p.length, p.width, p.height, p.weight), qty[pid])
        for pid, p in products.items()
    ]
    boxes = [_box_spec(b) for b in Box.objects.filter(is_active=True)]
    r = recommend_box(order_lines, boxes)

    data = {"status": r["status"]}
    if r["status"] == "too_many_units":
        data.update(total_units=r["total_units"], max_units=r["max_units"])
        return data
    data.update(total_units=r["total_units"], total_weight=float(r["total_weight"]),
                rejected_boxes=r["rejected"])
    if r["status"] == "ok":
        data.update(recommended_box=_box_json(r["recommended"]),
                    alternatives=[_box_json(b) for b in r["alternatives"]],
                    volume_utilization=round(r["volume_utilization"], 4))
    return data


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer


class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all().order_by("id")
    serializer_class = BoxSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related("items").order_by("id")
    serializer_class = OrderSerializer

    @action(detail=True, methods=["get"], url_path="recommend-box")
    def recommend_box(self, request, pk=None):
        order = self.get_object()
        lines = [(i.product_id, i.quantity) for i in order.items.all()]
        return Response(run_recommendation(lines))


class RecommendBoxView(APIView):
    def post(self, request):
        ser = RecommendRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        lines = [(i["product_id"], i["quantity"]) for i in ser.validated_data["items"]]
        return Response(run_recommendation(lines))
