from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupplierViewSet, PurchaseViewSet, StockViewSet
from . import views

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'stocks', StockViewSet) # Live Inventory Check karne ke liye

urlpatterns = [
    path('', include(router.urls)),
    path('purchases/<int:pk>/cancel/', views.cancel_purchase, name='cancel-purchase'),
]