import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Models import
from masters.models import Company, Salt, Medicine
from transactions.models import Supplier, PurchaseHeader, PurchaseItem, Stock

def seed_data():
    print("🌱 Seeding database with fresh test data...")

    # ==========================================
    # PHASE 2: MASTERS DATA
    # ==========================================
    
    # 1. Create Companies
    c1, _ = Company.objects.get_or_create(name="Cipla Ltd", defaults={'short_name': "CIP"})
    c2, _ = Company.objects.get_or_create(name="Sun Pharma", defaults={'short_name': "SUN"})
    c3, _ = Company.objects.get_or_create(name="Mankind Pharma", defaults={'short_name': "MAN"})
    c4, _ = Company.objects.get_or_create(name="Abbott India", defaults={'short_name': "ABB"})

    # 2. Create Salts
    s1, _ = Salt.objects.get_or_create(name="Paracetamol 500mg", defaults={'description': "Fever and pain relief"})
    s2, _ = Salt.objects.get_or_create(name="Amoxicillin 250mg", defaults={'description': "Antibiotic"})
    s3, _ = Salt.objects.get_or_create(name="Cetirizine 10mg", defaults={'description': "Allergy relief"})
    s4, _ = Salt.objects.get_or_create(name="Vitamin C 500mg", defaults={'description': "Immunity Booster"})

    # 3. Create Medicines
    m1, _ = Medicine.objects.update_or_create(
        name="Paracip 500", company=c1,
        defaults={'salt': s1, 'packing': '10X10', 'hsn_code': '3004', 'tax_percentage': Decimal('12.00')}
    )
    m2, _ = Medicine.objects.update_or_create(
        name="Moxikind-CV", company=c3,
        defaults={'salt': s2, 'packing': '10X6', 'hsn_code': '3004', 'tax_percentage': Decimal('12.00')}
    )
    m3, _ = Medicine.objects.update_or_create(
        name="Cetzine", company=c2,
        defaults={'salt': s3, 'packing': '15X10', 'hsn_code': '3004', 'tax_percentage': Decimal('12.00')}
    )
    m4, _ = Medicine.objects.update_or_create(
        name="Limcee Chewable", company=c4,
        defaults={'salt': s4, 'packing': '15X1', 'hsn_code': '3004', 'tax_percentage': Decimal('12.00')}
    )

    print("✅ Masters data seeded successfully!")

    # ==========================================
    # PHASE 3: TRANSACTIONS & STOCK DATA
    # ==========================================

    # 4. Create Suppliers (Distributors)
    sup1, _ = Supplier.objects.get_or_create(
        name="Delhi Pharma Distributors",
        defaults={'contact_no': '9876543210', 'gst_no': '07AAACD1234E1Z1'}
    )

    # 5. Create a Purchase Bill (Header)
    today = date.today()
    bill1, _ = PurchaseHeader.objects.get_or_create(
        bill_no="INV-1001", supplier=sup1,
        defaults={'bill_date': today, 'total_amount': Decimal('5000.00')}
    )

    # 6. Add Items to the Bill & Update Stock
    expiry_next_year = today.replace(year=today.year + 1)
    expiry_two_years = today.replace(year=today.year + 2)
    
    # Item 1: Paracip 500 (Batch 1)
    PurchaseItem.objects.get_or_create(
        purchase=bill1, medicine=m1, batch_no="B-CIP-001",
        defaults={'expiry_date': expiry_next_year, 'qty': 100, 'mrp': Decimal('35.00'), 'purchase_rate': Decimal('25.00')}
    )
    Stock.objects.update_or_create(
        medicine=m1, batch_no="B-CIP-001",
        defaults={'expiry_date': expiry_next_year, 'current_qty': 150, 'mrp': Decimal('35.00')}
    )

    # Item 2: Paracip 500 (Batch 2 - Alag expiry aur naya rate)
    Stock.objects.update_or_create(
        medicine=m1, batch_no="B-CIP-002",
        defaults={'expiry_date': expiry_two_years, 'current_qty': 80, 'mrp': Decimal('38.00')}
    )

    # Item 3: Moxikind-CV
    PurchaseItem.objects.get_or_create(
        purchase=bill1, medicine=m2, batch_no="B-MAN-099",
        defaults={'expiry_date': expiry_next_year, 'qty': 50, 'mrp': Decimal('150.00'), 'purchase_rate': Decimal('110.00')}
    )
    Stock.objects.update_or_create(
        medicine=m2, batch_no="B-MAN-099",
        defaults={'expiry_date': expiry_next_year, 'current_qty': 50, 'mrp': Decimal('150.00')}
    )

    # Item 4: Limcee
    Stock.objects.update_or_create(
        medicine=m4, batch_no="B-ABB-777",
        defaults={'expiry_date': expiry_two_years, 'current_qty': 200, 'mrp': Decimal('22.50')}
    )

    print("✅ Transactions & Stock data seeded successfully!")
    print("🚀 Database is ready! Ab aap Billing page par F2 dabakar test kar sakte hain.")

if __name__ == '__main__':
    seed_data()