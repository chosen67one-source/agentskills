"""
Example: Create a pay later payment
This script demonstrates how to create a new Afterpay or Klarna payment
"""

from pay_later import create_pay_later_payment


def create_afterpay_payment():
    """Create an Afterpay payment"""
    payment = create_pay_later_payment(
        amount=5000,  # $50.00
        currency="usd",
        payment_method="afterpay_pay_now",
        customer_email="customer@example.com",
        description="Shoes purchase",
        metadata={
            "order_id": "12345",
            "product": "Running Shoes",
        },
    )
    
    print("Afterpay Payment Created:")
    print(f"  Payment Intent ID: {payment['id']}")
    print(f"  Client Secret: {payment['client_secret']}")
    print(f"  Status: {payment['status']}")
    print(f"  Amount: {payment['amount']} {payment['currency'].upper()}")
    
    return payment


def create_klarna_payment():
    """Create a Klarna payment"""
    payment = create_pay_later_payment(
        amount=15000,  # $150.00
        currency="usd",
        payment_method="klarna",
        customer_email="customer@example.com",
        description="Electronics purchase",
        metadata={
            "order_id": "12346",
            "product": "Laptop",
        },
    )
    
    print("Klarna Payment Created:")
    print(f"  Payment Intent ID: {payment['id']}")
    print(f"  Client Secret: {payment['client_secret']}")
    print(f"  Status: {payment['status']}")
    
    return payment


if __name__ == "__main__":
    print("=== Afterpay Payment ===\n")
    create_afterpay_payment()
    
    print("\n=== Klarna Payment ===\n")
    create_klarna_payment()
