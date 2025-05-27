from django.urls import path
from . import views

app_name = 'heritage'


urlpatterns = [
    path('', views.home, name='home'),
    path('sites/', views.site_list, name='site_list'),
    path('site/<slug:slug>/', views.site_detail, name='site_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_site, name='create_site'),
    path('edit/<slug:slug>/', views.edit_site, name='site_edit'),
]
