"""
Stripe Pay Later Agent Skill

A comprehensive Agent Skill for handling Buy Now, Pay Later (BNPL)
and flexible payment transactions through Stripe.

Provides Python modules for:
- Payment intent creation and confirmation
- Payment method management
- Webhook handling
- Configuration management
"""

__version__ = "1.0.0"
__author__ = "agentskills"

from .pay_later import (
    create_pay_later_payment,
    confirm_payment,
    retrieve_payment,
    cancel_payment,
    get_payment_methods,
)
from .config import StripeConfig, PAYMENT_METHODS

__all__ = [
    "create_pay_later_payment",
    "confirm_payment",
    "retrieve_payment",
    "cancel_payment",
    "get_payment_methods",
    "StripeConfig",
    "PAYMENT_METHODS",
]
