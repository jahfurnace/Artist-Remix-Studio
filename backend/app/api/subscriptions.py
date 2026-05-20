import stripe
from app.core.config import settings
from fastapi import APIRouter, Request, HTTPException

stripe.api_key = settings.STRIPE_API_KEY
router = APIRouter()

@router.post("/create-checkout-session")
async def create_checkout_session(plan_id: str = "price_mock_123"):
    try:
        if not settings.STRIPE_API_KEY:
            # Mock successful response
            return {"url": "http://localhost:3000/dashboard?success=true"}
            
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': plan_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url='http://localhost:3000/dashboard?success=true',
            cancel_url='http://localhost:3000/pricing?canceled=true',
        )
        return {"url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get('Stripe-Signature')
    
    if not settings.STRIPE_WEBHOOK_SECRET:
        return {"status": "mock_success"}

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fulfill the purchase (e.g., upgrade user plan in DB)
        print("Payment successful for session:", session['id'])

    return {"status": "success"}
