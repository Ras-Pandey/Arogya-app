from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Hamari masters api ke routes yahan attach ho jayenge
    path('', include('masters.urls')), 
    # Phase 3: Transactions & Stock
    path('api/transactions/', include('transactions.urls')),
]