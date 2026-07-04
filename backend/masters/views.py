from rest_framework import viewsets
from .models import Company, Salt, Medicine
from .serializers import CompanySerializer, SaltSerializer, MedicineSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('-created_at')
    serializer_class = CompanySerializer

class SaltViewSet(viewsets.ModelViewSet):
    queryset = Salt.objects.all()
    serializer_class = SaltSerializer

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all().order_by('-created_at')
    serializer_class = MedicineSerializer