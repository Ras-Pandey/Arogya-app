from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, PurchaseViewSet, StockViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'stocks', StockViewSet) # Live Inventory Check karne ke liye

urlpatterns = [
    path('', include(router.urls)),
]