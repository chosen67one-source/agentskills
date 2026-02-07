"""
Stripe Pay Later - Core payment handling module
Handles creation and confirmation of pay later payments
"""

import os
import stripe
from typing import Dict, Any, Optional

# Initialize Stripe
stripe.api_key = os.environ.get("STRIPE_API_KEY")

if not stripe.api_key:
    raise ValueError("STRIPE_API_KEY environment variable is not set")


def create_pay_later_payment(
    amount: int,
    currency: str,
    payment_method: str,
    customer_email: str,
    description: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    return_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a pay later payment intent.
    
    Args:
        amount: Amount in cents (e.g., 10000 for $100.00)
        currency: Currency code (e.g., "usd")
        payment_method: One of: afterpay_pay_now, klarna, paypal, card
        customer_email: Customer email address
        description: Optional payment description
        metadata: Optional custom metadata dict
        return_url: Optional URL for redirect after confirmation
        
    Returns:
        Payment intent object
        
    Raises:
        stripe.error.InvalidRequestError: If parameters are invalid
        stripe.error.AuthenticationError: If API key is invalid
    """
    try:
        payment_intent_data = {
            "amount": amount,
            "currency": currency,
            "payment_method_types": [payment_method],
            "description": description or f"Pay later payment - {customer_email}",
            "receipt_email": customer_email,
            "metadata": metadata or {},
            "confirm": False,  # Don't auto-confirm, let customer authorize
        }
        
        if return_url:
            payment_intent_data["return_url"] = return_url
        
        payment_intent = stripe.PaymentIntent.create(**payment_intent_data)
        
        return {
            "id": payment_intent.id,
            "client_secret": payment_intent.client_secret,
            "status": payment_intent.status,
            "amount": payment_intent.amount,
            "currency": payment_intent.currency,
            "payment_method_types": payment_intent.payment_method_types,
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Failed to create payment: {str(e)}")


def confirm_payment(
    payment_intent_id: str,
    payment_method_id: Optional[str] = None,
    return_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Confirm a pay later payment.
    
    Args:
        payment_intent_id: The payment intent ID
        payment_method_id: Optional payment method ID to use
        return_url: Optional URL for redirect after confirmation
        
    Returns:
        Confirmed payment intent object
    """
    try:
        confirm_params = {}
        if payment_method_id:
            confirm_params["payment_method"] = payment_method_id
        if return_url:
            confirm_params["return_url"] = return_url
            
        payment_intent = stripe.PaymentIntent.confirm(
            payment_intent_id,
            **confirm_params
        )
        
        return {
            "id": payment_intent.id,
            "status": payment_intent.status,
            "client_secret": payment_intent.client_secret,
            "amount": payment_intent.amount,
            "charges": payment_intent.charges.data if payment_intent.charges else [],
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Failed to confirm payment: {str(e)}")


def retrieve_payment(payment_intent_id: str) -> Dict[str, Any]:
    """
    Retrieve payment intent details.
    
    Args:
        payment_intent_id: The payment intent ID
        
    Returns:
        Payment intent object
    """
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        return {
            "id": payment_intent.id,
            "status": payment_intent.status,
            "amount": payment_intent.amount,
            "currency": payment_intent.currency,
            "client_secret": payment_intent.client_secret,
            "payment_method": payment_intent.payment_method,
            "customer": payment_intent.customer,
            "created": payment_intent.created,
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Failed to retrieve payment: {str(e)}")


def cancel_payment(payment_intent_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
    """
    Cancel a payment intent.
    
    Args:
        payment_intent_id: The payment intent ID
        reason: Optional cancellation reason
        
    Returns:
        Cancelled payment intent object
    """
    try:
        cancel_params = {}
        if reason:
            cancel_params["cancellation_reason"] = reason
            
        payment_intent = stripe.PaymentIntent.cancel(
            payment_intent_id,
            **cancel_params
        )
        
        return {
            "id": payment_intent.id,
            "status": payment_intent.status,
            "cancellation_reason": payment_intent.cancellation_reason,
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Failed to cancel payment: {str(e)}")


def get_payment_methods(
    customer_id: str,
    limit: int = 10,
) -> Dict[str, Any]:
    """
    List payment methods for a customer.
    
    Args:
        customer_id: The Stripe customer ID
        limit: Number of results to return
        
    Returns:
        List of payment methods
    """
    try:
        payment_methods = stripe.PaymentMethod.list(
            customer=customer_id,
            limit=limit,
        )
        
        return {
            "object": "list",
            "data": [
                {
                    "id": pm.id,
                    "type": pm.type,
                    "billing_details": pm.billing_details,
                    "created": pm.created,
                }
                for pm in payment_methods.data
            ],
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Failed to retrieve payment methods: {str(e)}")
