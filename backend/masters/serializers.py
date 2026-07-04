from rest_framework import serializers
from .models import Company, Salt, Medicine

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class SaltSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salt
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    # Frontend par ID ke sath-sath company aur salt ka naam bhi dikhane ke liye
    company_name = serializers.ReadOnlyField(source='company.name')
    salt_name = serializers.ReadOnlyField(source='salt.name')
    
    class Meta:
        model = Medicine
        fields = '__all__'