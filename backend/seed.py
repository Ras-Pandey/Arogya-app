import os
import django

# Django environment setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from masters.models import Company, Salt, Medicine

def seed_data():
    print("Seeding dummy data...")
    
    # 1. Create Companies
    c1, _ = Company.objects.get_or_create(name="Cipla Limited", short_name="CIP")
    c2, _ = Company.objects.get_or_create(name="Sun Pharmaceutical", short_name="SUN")
    c3, _ = Company.objects.get_or_create(name="Mankind Pharma", short_name="MAN")
    
    # 2. Create Salts
    s1, _ = Salt.objects.get_or_create(name="Paracetamol 500mg", description="Fever and pain relief")
    s2, _ = Salt.objects.get_or_create(name="Amoxicillin 250mg", description="Antibiotic")
    
    # 3. Create Medicines
    Medicine.objects.get_or_create(name="Dolo 500", company=c1, salt=s1, packing="15X10", hsn_code="3004")
    Medicine.objects.get_or_create(name="Mox 250", company=c2, salt=s2, packing="10X10", hsn_code="3004")
    
    print("Data seeded successfully! Arogya-App is ready for testing.")

if __name__ == '__main__':
    seed_data()