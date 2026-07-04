from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, SaltViewSet, MedicineViewSet

# Router automatically saari CRUD APIs ke routes bana deta hai
router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'salts', SaltViewSet)
router.register(r'medicines', MedicineViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]