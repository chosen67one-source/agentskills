"""
Configuration and environment setup for Stripe Pay Later
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class StripeConfig:
    """Stripe configuration"""
    
    # API Keys
    api_key: str
    publishable_key: str
    webhook_secret: Optional[str] = None
    
    # Payment settings
    default_currency: str = "usd"
    default_return_url: Optional[str] = None
    
    # Retry settings
    max_retries: int = 3
    retry_delay: int = 1  # seconds
    
    @classmethod
    def from_env(cls) -> "StripeConfig":
        """Load configuration from environment variables"""
        api_key = os.environ.get("STRIPE_API_KEY")
        if not api_key:
            raise ValueError("STRIPE_API_KEY environment variable is required")
        
        publishable_key = os.environ.get("STRIPE_PUBLISHABLE_KEY")
        if not publishable_key:
            raise ValueError("STRIPE_PUBLISHABLE_KEY environment variable is required")
        
        return cls(
            api_key=api_key,
            publishable_key=publishable_key,
            webhook_secret=os.environ.get("STRIPE_WEBHOOK_SECRET"),
            default_currency=os.environ.get("STRIPE_CURRENCY", "usd"),
            default_return_url=os.environ.get("STRIPE_RETURN_URL"),
            max_retries=int(os.environ.get("STRIPE_MAX_RETRIES", "3")),
            retry_delay=int(os.environ.get("STRIPE_RETRY_DELAY", "1")),
        )


# Payment method types
PAYMENT_METHODS = {
    "afterpay_pay_now": "Afterpay Pay Now",
    "klarna": "Klarna",
    "paypal": "PayPal",
    "card": "Card",
}

# Test API keys map (for development)
TEST_KEYS = {
    "sk_test_51SxyGKLAiVLuV6Wk": "Test Secret Key",
    "pk_test_51SxyGKLAiVLuV6Wk": "Test Publishable Key",
}
