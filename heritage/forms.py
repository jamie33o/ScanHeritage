from django import forms
from .models import HeritageSite, SiteImage, SiteFact

class HeritageSiteForm(forms.ModelForm):
    class Meta:
        model = HeritageSite
        exclude = ['owner', 'slug', 'qr_code', 'created_at', 'updated_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'site_type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'established_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'historical_period': forms.TextInput(attrs={'class': 'form-control'}),
            'architect': forms.TextInput(attrs={'class': 'form-control'}),
            'historical_significance': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'hours_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SiteImageForm(forms.ModelForm):
    class Meta:
        model = SiteImage
        fields = ['image', 'caption', 'order']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SiteFactForm(forms.ModelForm):
    class Meta:
        model = SiteFact
        fields = ['title', 'description', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }