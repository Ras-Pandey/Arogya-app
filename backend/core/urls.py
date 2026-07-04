from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')), # Auth route added[cite: 1, 4]
    path('', include('masters.urls')), 
    path('api/transactions/', include('transactions.urls')),
]