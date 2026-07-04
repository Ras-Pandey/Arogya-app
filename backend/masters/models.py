from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Salt(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='medicines')
    salt = models.ForeignKey(Salt, on_delete=models.SET_NULL, null=True, blank=True, related_name='medicines')
    
    # Pharma specific fields
    packing = models.CharField(max_length=50, help_text="e.g., 10X10, 1X15, 100ML")
    hsn_code = models.CharField(max_length=20, blank=True, null=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=12.00, help_text="GST percentage")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.packing}"