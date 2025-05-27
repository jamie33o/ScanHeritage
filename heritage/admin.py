from django.contrib import admin
from .models import Category, HeritageSite, SiteImage, SiteFact

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

class SiteImageInline(admin.TabularInline):
    model = SiteImage
    extra = 1

class SiteFactInline(admin.TabularInline):
    model = SiteFact
    extra = 1

@admin.register(HeritageSite)
class HeritageSiteAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'site_type', 'city', 'state', 'is_published', 'featured', 'created_at']
    list_filter = ['site_type', 'is_published', 'featured', 'created_at', 'category']
    search_fields = ['title', 'city', 'state', 'description']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SiteImageInline, SiteFactInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'title', 'slug', 'site_type', 'category', 'description', 'short_description', 'main_image')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'country', 'latitude', 'longitude')
        }),
        ('Historical Information', {
            'fields': ('established_year', 'historical_period', 'architect', 'historical_significance')
        }),
        ('Contact & Hours', {
            'fields': ('website', 'phone', 'email', 'hours_info')
        }),
        ('Publishing', {
            'fields': ('is_published', 'featured')
        }),
    )