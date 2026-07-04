from rest_framework import serializers
from .models import Supplier, PurchaseHeader, PurchaseItem, Stock

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    # Stock me dawai ka naam direct dikhane ke liye
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    
    class Meta:
        model = Stock
        fields = '__all__'

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem
        fields = ['id', 'medicine', 'batch_no', 'expiry_date', 'qty', 'mrp', 'purchase_rate']

class PurchaseHeaderSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many=True) # Nested items

    class Meta:
        model = PurchaseHeader
        fields = ['id', 'supplier', 'bill_no', 'bill_date', 'total_amount', 'items']

    # THE MAGIC TRIGGER: Bill save hote hi Stock update karna
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        purchase = PurchaseHeader.objects.create(**validated_data)
        
        for item_data in items_data:
            # 1. Bill me item add karo
            PurchaseItem.objects.create(purchase=purchase, **item_data)
            
            # 2. Stock Godam me dawai Plus (+) karo
            stock, created = Stock.objects.get_or_create(
                medicine=item_data['medicine'],
                batch_no=item_data['batch_no'],
                defaults={
                    'expiry_date': item_data['expiry_date'],
                    'current_qty': 0,
                    'mrp': item_data['mrp']
                }
            )
            stock.current_qty += item_data['qty']
            stock.save()

        return purchase