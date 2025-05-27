from django.db import models
from django.contrib.auth.models import User
from heritage.models import HeritageSite

class QRSignProduct(models.Model):
    MATERIALS = [
        ('aluminum', 'Aluminum'),
        ('acrylic', 'Acrylic'),
        ('wood', 'Wood'),
        ('steel', 'Stainless Steel'),
    ]
    
    SIZES = [
        ('small', '6" x 4"'),
        ('medium', '8" x 6"'),
        ('large', '12" x 8"'),
        ('xlarge', '16" x 12"'),
    ]
    
    name = models.CharField(max_length=200)
    material = models.CharField(max_length=20, choices=MATERIALS)
    size = models.CharField(max_length=20, choices=SIZES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_material_display()} ({self.get_size_display()})"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Shipping Information
    shipping_name = models.CharField(max_length=200)
    shipping_email = models.EmailField()
    shipping_phone = models.CharField(max_length=20)
    shipping_address = models.CharField(max_length=300)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100, default='United States')
    
    # Payment
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    heritage_site = models.ForeignKey(HeritageSite, on_delete=models.CASCADE)
    product = models.ForeignKey(QRSignProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Custom text for the sign
    custom_text = models.TextField(blank=True, help_text="Additional text to include on the sign")
    
    def __str__(self):
        return f"{self.product.name} for {self.heritage_site.title}"
    
    @property
    def total_price(self):
        return self.price * self.quantity