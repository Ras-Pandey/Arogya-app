from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

# Naye imports Phase 4 (Invoice) ke liye add kiye gaye hain
from .models import Supplier, PurchaseHeader, Stock, Invoice, InvoiceItem
from .serializers import SupplierSerializer, PurchaseHeaderSerializer, StockSerializer
from masters.models import Medicine

# ==========================================
# PHASE 2 & 3: MASTERS & PURCHASE VIEWS
# ==========================================
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


# ==========================================
# PHASE 4: BILLING ENGINE & POS VIEWS
# ==========================================
class AvailableStockView(APIView):
    """
    Ye API POS screen ke F2 search ke liye active stock (qty > 0) fetch karti hai.
    """
    def get(self, request):
        stocks = Stock.objects.filter(current_qty__gt=0).select_related('medicine')
        data = []
        for s in stocks:
            data.append({
                'stock_id': s.id,
                'medicine_id': s.medicine.id,
                'name': s.medicine.name,
                'batch_no': s.batch_no,
                'expiry_date': s.expiry_date.strftime('%Y-%m-%d') if s.expiry_date else None,
                'mrp': float(s.mrp),
                'stock': s.current_qty
            })
        return Response(data, status=status.HTTP_200_OK)


class InvoiceCreateView(APIView):
    """
    Ye API final bill (invoice) save karti hai aur stock minus karti hai.
    """
    def post(self, request):
        data = request.data
        try:
            with transaction.atomic():
                # 1. Create Invoice Header
                invoice = Invoice.objects.create(
                    invoice_number=data['invoice_number'],
                    customer_name=data.get('customer_name', ''),
                    total_amount=data['total_amount'],
                    gst_amount=data.get('gst_amount', 0),
                    net_payable=data['net_payable']
                )

                # 2. Add Items & Deduct Stock
                for item in data['items']:
                    medicine = Medicine.objects.get(id=item['medicine_id'])
                    batch_no = item['batch_no']
                    qty_to_sell = int(item['quantity'])

                    # Fetch specific batch from Stock
                    stock_item = Stock.objects.get(medicine=medicine, batch_no=batch_no)
                    
                    if stock_item.current_qty < qty_to_sell:
                        raise ValueError(f"Insufficient stock for {medicine.name} (Batch: {batch_no})")

                    # Deduct Stock
                    stock_item.current_qty -= qty_to_sell
                    stock_item.save()

                    # Save line item
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        medicine=medicine,
                        batch_no=batch_no,
                        quantity=qty_to_sell,
                        rate=item['rate'],
                        amount=item['amount']
                    )

            return Response({"message": "Bill saved and stock updated!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)