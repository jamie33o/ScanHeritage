from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from heritage.models import HeritageSite
from .models import QRSignProduct, OrderItem
from .forms import OrderForm
from django.contrib import messages
import stripe

# Create your views here.

@login_required
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

def product_list(request):
    products = QRSignProduct.objects.filter(is_active=True)
    return render(request, 'orders/product_list.html', {'products': products})


@login_required
def order_qr_sign(request, site_slug):
    site = get_object_or_404(HeritageSite, slug=site_slug, owner=request.user)
    products = QRSignProduct.objects.filter(is_active=True)
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        custom_text = request.POST.get('custom_text', '')
        
        product = get_object_or_404(QRSignProduct, id=product_id)
        
        # Store in session for checkout
        request.session['order_data'] = {
            'site_id': site.id,
            'product_id': product.id,
            'quantity': quantity,
            'custom_text': custom_text,
            'total_amount': float(product.price * quantity)
        }
        
        return redirect('orders:checkout')
    
    context = {
        'site': site,
        'products': products,
    }
    return render(request, 'orders/order_qr_sign.html', context)


@login_required
def checkout(request):
    order_data = request.session.get('order_data')
    if not order_data:
        messages.error(request, 'No order data found.')
        return redirect('heritage:dashboard')
    
    site = get_object_or_404(HeritageSite, id=order_data['site_id'])
    product = get_object_or_404(QRSignProduct, id=order_data['product_id'])
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create Stripe Payment Intent
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(order_data['total_amount'] * 100),  # Convert to cents
                    currency='usd',
                    metadata={
                        'user_id': request.user.id,
                        'site_slug': site.slug,
                        'product_id': product.id,
                    }
                )
                
                # Create Order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=order_data['total_amount'],
                    stripe_payment_intent_id=intent.id,
                    **form.cleaned_data
                )
                
                # Create Order Item
                OrderItem.objects.create(
                    order=order,
                    heritage_site=site,
                    product=product,
                    quantity=order_data['quantity'],
                    price=product.price,
                    custom_text=order_data['custom_text']
                )
                
                # Clear session data
                del request.session['order_data']
                
                return render(request, 'orders/payment.html', {
                    'client_secret': intent.client_secret,
                    'order': order,
                    'publishable_key': settings.STRIPE_PUBLISHABLE_KEY
                })
                
            except stripe.error.StripeError as e:
                messages.error(request, f'Payment error: {str(e)}')
                
    else:
        # Pre-fill form with user data if available
        initial_data = {}
        if hasattr(request.user, 'userprofile'):
            profile = request.user.userprofile
            initial_data = {
                'shipping_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'shipping_email': request.user.email,
                'shipping_phone': profile.phone,
                'shipping_address': profile.address,
                'shipping_city': profile.city,
                'shipping_state': profile.state,
                'shipping_zip': profile.zip_code,
                'shipping_country': profile.country,
            }
        else:
            initial_data = {
                'shipping_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'shipping_email': request.user.email,
                'shipping_country': 'United States',
            }
        
        form = OrderForm(initial=initial_data)
    
    context = {
        'form': form,
        'site': site,
        'product': product,
        'order_data': order_data,
    }
    return render(request, 'orders/checkout.html', context)