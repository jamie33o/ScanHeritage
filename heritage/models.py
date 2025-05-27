from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class HeritageSite(models.Model):
    SITE_TYPES = [
        ('town', 'Town'),
        ('landmark', 'Landmark'),
        ('building', 'Historic Building'),
        ('monument', 'Monument'),
        ('museum', 'Museum'),
        ('other', 'Other'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    site_type = models.CharField(max_length=20, choices=SITE_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Basic Information
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text="Brief description for previews")
    
    # Location
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="United States")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Historical Information
    established_year = models.IntegerField(null=True, blank=True)
    historical_period = models.CharField(max_length=100, blank=True)
    architect = models.CharField(max_length=200, blank=True)
    historical_significance = models.TextField(blank=True)
    
    # Images
    main_image = models.ImageField(upload_to='heritage/images/', null=True, blank=True)
    
    # Contact & Hours
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    hours_info = models.TextField(blank=True, help_text="Operating hours information")
    
    # QR Code
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    
    # Meta
    is_published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('heritage:site_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Generate QR code
        if not self.qr_code:
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"https://scanheritage.com{self.get_absolute_url()}")
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            file_name = f'qr_{self.slug}.png'
            self.qr_code.save(file_name, File(buffer), save=False)
            buffer.close()
        
        super().save(*args, **kwargs)

class SiteImage(models.Model):
    site = models.ForeignKey(HeritageSite, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='heritage/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']

class SiteFact(models.Model):
    site = models.ForeignKey(HeritageSite, on_delete=models.CASCADE, related_name='facts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']