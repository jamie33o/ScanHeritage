from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('order/<slug:site_slug>/', views.order_qr_sign, name='order_qr_sign'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/<str:order_number>/', views.order_success, name='order_success'),
    path('history/', views.order_history, name='order_history'),
]