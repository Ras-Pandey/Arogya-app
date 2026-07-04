from django.db import models
from masters.models import Medicine

# 1. Jis distributor se maal aata hai
class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_no = models.CharField(max_length=20, blank=True, null=True)
    gst_no = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.name

# 2. Purchase Bill (Header detail)
class PurchaseHeader(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    bill_no = models.CharField(max_length=50)
    bill_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bill_no} - {self.supplier.name}"

# 3. Bill ke andar ki dawaiyan
class PurchaseItem(models.Model):
    purchase = models.ForeignKey(PurchaseHeader, related_name='items', on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)
    batch_no = models.CharField(max_length=50)
    expiry_date = models.DateField()
    qty = models.IntegerField(default=0)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_rate = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.medicine.name} ({self.batch_no})"

# 4. Asli Godam (Jahan F10 dabane par stock plus hoga)
class Stock(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    batch_no = models.CharField(max_length=50)
    expiry_date = models.DateField()
    current_qty = models.IntegerField(default=0)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('medicine', 'batch_no')

    def __str__(self):
        return f"{self.medicine.name} - {self.batch_no} (Qty: {self.current_qty})"