import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Apne models import karein
from masters.models import Company, Salt, Medicine
from transactions.models import Supplier, PurchaseHeader, PurchaseItem, Stock

def seed_data():
    print("Seeding database with fresh data...")

    # ==========================================
    # PHASE 2: MASTERS DATA
    # ==========================================
    
    # 1. Create Companies
    c1, _ = Company.objects.get_or_create(name="Cipla Ltd", short_name="CIP")
    c2, _ = Company.objects.get_or_create(name="Sun Pharma", short_name="SUN")
    c3, _ = Company.objects.get_or_create(name="Mankind Pharma", short_name="MAN")

    # 2. Create Salts
    s1, _ = Salt.objects.get_or_create(name="Paracetamol 500mg", description="Fever and pain relief")
    s2, _ = Salt.objects.get_or_create(name="Amoxicillin 250mg", description="Antibiotic")
    s3, _ = Salt.objects.get_or_create(name="Cetirizine 10mg", description="Allergy relief")

    # 3. Create Medicines
    m1, _ = Medicine.objects.get_or_create(
        name="Paracip 500", company=c1, salt=s1,
        defaults={'packing': '10X10', 'hsn_code': '3004', 'tax_percentage': Decimal('12.00')}
    )
    m2, _ = Medicine.objects.get_or_create(
        name="Moxikind-CV", company=c3, salt=s2,
        defaults={'packing': '10X6', 'hsn_code': '3004', 'tax_percentage': Decimal('12.00')}
    )
    m3, _ = Medicine.objects.get_or_create(
        name="Cetzine", company=c2, salt=s3,
        defaults={'packing': '15X10', 'hsn_code': '3004', 'tax_percentage': Decimal('12.00')}
    )

    print("Masters data seeded successfully!")

    # ==========================================
    # PHASE 3: TRANSACTIONS & STOCK DATA
    # ==========================================

    # 4. Create Suppliers (Distributors)
    sup1, _ = Supplier.objects.get_or_create(
        name="Delhi Pharma Distributors",
        defaults={'contact_no': '9876543210', 'gst_no': '07AAACD1234E1Z1'}
    )
    sup2, _ = Supplier.objects.get_or_create(
        name="Apollo Medical Suppliers",
        defaults={'contact_no': '9988776655', 'gst_no': '07BBBBA4321E1Z2'}
    )

    # 5. Create a Purchase Bill (Header)
    today = date.today()
    bill1, created = PurchaseHeader.objects.get_or_create(
        bill_no="INV-1001",
        supplier=sup1,
        defaults={'bill_date': today, 'total_amount': Decimal('2500.00')}
    )

    # 6. Add Items to the Bill & Update Stock (Simulating the trigger)
    if created:
        expiry_next_year = today.replace(year=today.year + 1)
        
        # Item 1: Paracip 500
        PurchaseItem.objects.create(
            purchase=bill1, medicine=m1, batch_no="B-CIP-001", expiry_date=expiry_next_year,
            qty=50, mrp=Decimal('35.00'), purchase_rate=Decimal('25.00')
        )
        Stock.objects.get_or_create(
            medicine=m1, batch_no="B-CIP-001",
            defaults={'expiry_date': expiry_next_year, 'current_qty': 50, 'mrp': Decimal('35.00')}
        )

        # Item 2: Moxikind-CV
        PurchaseItem.objects.create(
            purchase=bill1, medicine=m2, batch_no="B-MAN-099", expiry_date=expiry_next_year,
            qty=20, mrp=Decimal('150.00'), purchase_rate=Decimal('110.00')
        )
        Stock.objects.get_or_create(
            medicine=m2, batch_no="B-MAN-099",
            defaults={'expiry_date': expiry_next_year, 'current_qty': 20, 'mrp': Decimal('150.00')}
        )

    print("Transactions & Stock data seeded successfully!")
    print("Database is ready for testing!")

if __name__ == '__main__':
    seed_data()