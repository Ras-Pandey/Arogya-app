from rest_framework import viewsets
from .models import Supplier, PurchaseHeader, Stock
from .serializers import SupplierSerializer, PurchaseHeaderSerializer, StockSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('name')
    serializer_class = SupplierSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = PurchaseHeader.objects.all().order_by('-bill_date', '-id')
    serializer_class = PurchaseHeaderSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all().order_by('medicine__name')
    serializer_class = StockSerializer