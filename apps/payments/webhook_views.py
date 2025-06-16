import stripe
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from .models import PaymentTransaction
from apps.orders.models import Order

@csrf_exempt
def stripe_webhook(request):
    print(" Webhook endpoint called")
    print("Request method:", request.method)
    print("Headers:", request.headers)
    print("Body:", request.body)
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        print("Webhook Error: ", e)
        return HttpResponse(status=400)

    print(" Event received: ", json.dumps(event, indent=2))

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        try:
            intent = stripe.PaymentIntent.retrieve(session['payment_intent'])
            print("Retrieved Payment Intent: ", json.dumps(intent, indent=2))
            handle_checkout_session_completed(session, intent)
        except Exception as e:
            # Log error if needed
            print("Error handling checkout session: ", e)
            pass

    elif event['type'] == 'payment_intent.payment_failed':
        session = event['data']['object']
        print("Payment Failed: ", json.dumps(session, indent=2))
        handle_payment_failed(session)

    return HttpResponse(status=200)


def handle_checkout_session_completed(session, intent):
    session_id = session.get('id')
    intent_id = intent.get('id')
    status = intent.get('status')

    try:
        transaction = PaymentTransaction.objects.get(stripe_checkout_session_id=session_id)
        transaction.stripe_payment_intent = intent_id
        transaction.status = status
        transaction.save()

        if status == 'succeeded' and transaction.order:
            transaction.order.status = 'processing'
            transaction.order.save()
    except PaymentTransaction.DoesNotExist:
        pass


def handle_payment_failed(session):
    intent_id = session.get('id')
    try:
        transaction = PaymentTransaction.objects.get(stripe_payment_intent=intent_id)
        transaction.status = 'failed'
        transaction.save()

        if transaction.order:
            transaction.order.status = 'cancelled'
            transaction.order.save()
    except PaymentTransaction.DoesNotExist:
        pass
