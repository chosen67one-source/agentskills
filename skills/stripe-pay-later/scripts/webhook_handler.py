"""
Stripe Pay Later - Webhook Handler
Handles incoming Stripe events like payment confirmation, refunds, etc.
"""

import os
import json
import stripe
from flask import Flask, request
from typing import Tuple, Dict, Any

app = Flask(__name__)

# Initialize Stripe
stripe.api_key = os.environ.get("STRIPE_API_KEY")
WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

if not WEBHOOK_SECRET:
    print("WARNING: STRIPE_WEBHOOK_SECRET not set. Webhook verification will fail.")


def handle_payment_intent_succeeded(event: Dict[str, Any]) -> None:
    """Handle successful payment intent"""
    payment_intent = event["data"]["object"]
    print(f"Payment succeeded: {payment_intent['id']}")
    # Add your business logic here
    # - Update order status to "paid"
    # - Send confirmation email
    # - Trigger fulfillment process


def handle_payment_intent_failed(event: Dict[str, Any]) -> None:
    """Handle failed payment intent"""
    payment_intent = event["data"]["object"]
    print(f"Payment failed: {payment_intent['id']}")
    # Add your business logic here
    # - Update order status to "failed"
    # - Send failure notification
    # - Trigger retry logic


def handle_charge_refunded(event: Dict[str, Any]) -> None:
    """Handle charge refund"""
    charge = event["data"]["object"]
    print(f"Charge refunded: {charge['id']}")
    # Add your business logic here
    # - Update order status to "refunded"
    # - Send refund confirmation
    # - Schedule return shipment


@app.route("/webhook", methods=["POST"])
def webhook() -> Tuple[str, int]:
    """
    Stripe webhook endpoint
    
    Expected headers:
    - stripe-signature: Stripe signature for verification
    
    Security:
    - Verifies webhook signature using WEBHOOK_SECRET
    - Only processes recognized event types
    """
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("stripe-signature")
    
    # Verify webhook signature
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except ValueError as e:
        print(f"Invalid payload: {e}")
        return "400 Bad Request", 400
    except stripe.error.SignatureVerificationError as e:
        print(f"Invalid signature: {e}")
        return "403 Forbidden", 403
    
    # Handle the event
    event_type = event["type"]
    
    try:
        if event_type == "payment_intent.succeeded":
            handle_payment_intent_succeeded(event)
        elif event_type == "payment_intent.payment_failed":
            handle_payment_intent_failed(event)
        elif event_type == "charge.refunded":
            handle_charge_refunded(event)
        else:
            print(f"Unhandled event type: {event_type}")
    except Exception as e:
        print(f"Error handling event: {e}")
        return "500 Internal Server Error", 500
    
    return "200 OK", 200


@app.route("/webhook/status", methods=["GET"])
def webhook_status():
    """Health check endpoint"""
    return {"status": "ok", "webhook": "stripe-pay-later"}


if __name__ == "__main__":
    # Development only - use a production WSGI server in production
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
