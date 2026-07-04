from rest_framework import viewsets
from .models import Supplier, PurchaseHeader, Stock
from .serializers import SupplierSerializer, PurchaseHeaderSerializer, StockSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PurchaseHeader, Stock

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('name')
    serializer_class = SupplierSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = PurchaseHeader.objects.all().order_by('-bill_date', '-id')
    serializer_class = PurchaseHeaderSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all().order_by('medicine__name')
    serializer_class = StockSerializer

@api_view(['POST'])
def cancel_purchase(request, pk):
    purchase = get_object_or_404(PurchaseHeader, pk=pk)
    
    
    if purchase.is_cancelled:
        return Response({"error": "Already cancelled"}, status=400)
    
    for item in purchase.items.all():
        stock = Stock.objects.get(medicine=item.medicine, batch_no=item.batch_no)
        stock.current_qty -= item.qty 
        stock.save()
        
    purchase.is_cancelled = True
    purchase.save()
    
    return Response({"message": "Cancelled"})