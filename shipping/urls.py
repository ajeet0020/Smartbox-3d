from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BoxViewSet, OrderViewSet, ProductViewSet, RecommendBoxView

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("boxes", BoxViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("recommend-box/", RecommendBoxView.as_view()),
    path("", include(router.urls)),
]
