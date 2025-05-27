
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import stripe
from decouple import config
from orders.models import Order
# Stripe webhook to handle payment confirmation
# Additional view for payment confirmation webhook
@require_http_methods(["POST"])
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = config('STRIPE_WEBHOOK_SECRET', default='')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the payment_intent.succeeded event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        try:
            order = Order.objects.get(stripe_payment_intent_id=payment_intent['id'])
            order.status = 'processing'
            order.save()
            
            # Send confirmation email here if needed
            
        except Order.DoesNotExist:
            pass

    return HttpResponse(status=200)