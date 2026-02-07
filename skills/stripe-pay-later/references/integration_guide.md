# Stripe Pay Later Integration Guide

## Quick Start (5 minutes)

### 1. Get Your API Keys

1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Sign in or create a new account
3. Navigate to Developers > API keys
4. Copy your **Secret Key** (starts with `sk_live_` or `sk_test_`)
5. Copy your **Publishable Key** (starts with `pk_live_` or `pk_test_`)

### 2. Set Up Environment Variables

```bash
# Create .env file
export STRIPE_API_KEY="sk_test_your_key_here"
export STRIPE_PUBLISHABLE_KEY="pk_test_your_key_here"
export STRIPE_WEBHOOK_SECRET="whsec_test_your_secret"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Test the Integration

```bash
python scripts/create_payment.py
```

---

## Full Setup Instructions

### Prerequisites

- Python 3.8+
- Active Stripe account
- Stripe API keys (develop sandbox, then move to production)

### Account Setup

#### Enable Pay Later Methods

1. Log into Stripe Dashboard
2. Go to **Settings > Payment methods**
3. Enable desired methods:
   - Afterpay
   - Klarna
   - PayPal
   
4. Configure regional settings based on your business
5. Set up timezone and currency preferences

#### Webhook Configuration

1. Go to **Developers > Webhooks**
2. Click **Add endpoint**
3. Enter your webhook URL: `https://your-domain.com/webhook`
4. Select events to listen for:
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
   - `charge.refunded`
5. Copy the webhook signing secret
6. Add to environment: `STRIPE_WEBHOOK_SECRET`

### Installation

```bash
# Clone or navigate to skill directory
cd skills/stripe-pay-later

# Install dependencies
pip install -r requirements.txt

# Load environment variables
source .env  # or export them manually
```

### Configuration

#### Environment Variables Required

```
STRIPE_API_KEY              # Secret key from Stripe
STRIPE_PUBLISHABLE_KEY      # Publishable key from Stripe
STRIPE_WEBHOOK_SECRET       # Webhook signing secret
STRIPE_CURRENCY             # Optional: default currency (default: usd)
STRIPE_RETURN_URL          # Optional: post-payment redirect URL
STRIPE_MAX_RETRIES         # Optional: retry attempts (default: 3)
STRIPE_RETRY_DELAY         # Optional: delay between retries in seconds
```

#### Using .env File

Create a `.env` file in the skill directory:

```
STRIPE_API_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_test_...
STRIPE_CURRENCY=usd
STRIPE_RETURN_URL=https://yourdomain.com/payment-success
```

Load it in your Python code:

```python
from dotenv import load_dotenv
load_dotenv()
```

### Testing

#### Test Mode vs. Live Mode

**Test Mode:**
- Use secret key: `sk_test_*`
- Use publishable key: `pk_test_*`
- No real money is processed
- Use test cards: 4242 4242 4242 4242

**Live Mode:**
- Use secret key: `sk_live_*`
- Use publishable key: `pk_live_*`
- Real money is processed
- Requires PCI compliance

#### Test Credit Cards

```
Card Number: 4242 4242 4242 4242
Expiry: 12/34
CVC: 123
```

#### Test Afterpay

```
Card: 4242 4242 4242 4242
Expiry: 12/34
CVC: 123
```

#### Test Klarna

Test Klarna by processing through the payment flow - Stripe will handle simulated Klarna authorization.

---

## Implementation Examples

### Simple Payment Flow

```python
from scripts.pay_later import (
    create_pay_later_payment,
    confirm_payment,
    retrieve_payment
)

# Step 1: Create payment intent
payment = create_pay_later_payment(
    amount=10000,  # $100.00
    currency="usd",
    payment_method="afterpay_pay_now",
    customer_email="user@example.com"
)

print(f"Payment created: {payment['id']}")

# Step 2: Customer authorizes on provider's site
# (User is redirected to Afterpay/Klarna)

# Step 3: Confirm payment
confirmation = confirm_payment(payment['id'])
print(f"Payment status: {confirmation['status']}")

# Step 4: Check payment status
details = retrieve_payment(payment['id'])
print(f"Final status: {details['status']}")
```

### Building a Checkout

```python
# 1. Create payment intent
payment_intent = create_pay_later_payment(
    amount=cart_total,
    currency="usd",
    payment_method=selected_method,  # "afterpay_pay_now", "klarna", etc.
    customer_email=email,
    description=f"Order: {order_id}",
    metadata={
        "order_id": order_id,
        "customer_id": customer_id
    },
    return_url="https://yoursite.com/payment-success"
)

# 2. Pass client_secret to frontend
return {
    "client_secret": payment_intent["client_secret"],
    "payment_intent_id": payment_intent["id"]
}

# 3. Frontend handles redirect and confirmation
# 4. Use webhook to confirm completion
```

### Handling Refunds

```python
from scripts.pay_later import retrieve_payment
import stripe

# Get payment details
payment = retrieve_payment("pi_1234567890")

# Create refund
refund = stripe.Refund.create(
    charge=payment['charges'][0]['id'],
    reason="customer_request"
)

# Webhook will trigger charge.refunded event
```

---

## Production Deployment

### Pre-Launch Checklist

- [ ] Switch from test keys to live keys
- [ ] Test with real payment methods (small amount)
- [ ] Enable webhook HTTPS with valid SSL
- [ ] Implement comprehensive error handling
- [ ] Set up logging and monitoring
- [ ] Configure email notifications
- [ ] Test refund process
- [ ] Document payment flow for support team
- [ ] Set up PCI compliance measures
- [ ] Configure rate limiting

### Security Checklist

- [ ] Never log or expose API keys
- [ ] Use environment variables for secrets
- [ ] Verify webhook signatures
- [ ] Implement HTTPS only
- [ ] Use strong webhook validation
- [ ] Implement request/response logging
- [ ] Set up fraud detection
- [ ] Monitor for suspicious activity
- [ ] Regular security audits
- [ ] Keep libraries updated

### Monitoring

```python
# Example: Set up logging
import logging

logger = logging.getLogger("stripe_payments")
handler = logging.FileHandler("stripe_payments.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Log important events
logger.info(f"Payment created: {payment_id}")
logger.error(f"Payment failed: {error_message}")
```

---

## Troubleshooting

### Issue: "Authentication Failed"

**Solution:**
- Verify STRIPE_API_KEY is set correctly
- Make sure you're using the right key (test vs. live)
- Check for whitespace or typos in the key

### Issue: "Invalid Request"

**Solution:**
- Verify amount is in cents (e.g., 10000 for $100)
- Ensure currency code is valid (e.g., "usd")
- Check that payment_method is supported

### Issue: "Webhook Not Received"

**Solution:**
- Verify webhook URL is publicly accessible
- Check STRIPE_WEBHOOK_SECRET matches
- Inspect Stripe dashboard webhook logs
- Ensure endpoint returns 200 status

### Issue: "Customer Not Found"

**Solution:**
- Create customer first: `stripe.Customer.create(email="...")`
- Use returned customer ID in payment intent

---

## Resources

- [Stripe Dashboard](https://dashboard.stripe.com)
- [Stripe Python Library](https://github.com/stripe/stripe-python)
- [API Documentation](https://stripe.com/docs/api)
- [Afterpay Integration](https://stripe.com/docs/payments/afterpay)
- [Klarna Integration](https://stripe.com/docs/payments/klarna)
- [Webhook Events](https://stripe.com/docs/api/events)
- [Error Codes](https://stripe.com/docs/error-codes)
