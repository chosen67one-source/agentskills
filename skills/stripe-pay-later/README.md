# Stripe Pay Later Skill

This Agent Skill enables AI agents to process Buy Now, Pay Later (BNPL) and flexible payment transactions through Stripe.

## Features

✅ **Multiple Payment Methods**
- Afterpay - Pay in 4 interest-free installments
- Klarna - Flexible payment options
- PayPal - BNPL and standard payments
- Credit/Debit Cards - Traditional payment processing

✅ **Payment Operations**
- Create payment intents
- Confirm payments
- Retrieve payment status
- Cancel payments
- Manage payment methods
- Process refunds

✅ **Webhooks**
- Listen for payment events
- Handle payment status updates
- Automatic notification system

## Quick Start

### 1. Copy .env Configuration

```bash
cp .env.example .env
```

### 2. Add Your Stripe Keys

Get your keys from [Stripe Dashboard](https://dashboard.stripe.com/apikeys):

```bash
STRIPE_API_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_test_...
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Try a Test Payment

```bash
python scripts/create_payment.py
```

## Project Structure

```
stripe-pay-later/
├── SKILL.md                    # Agent Skills specification
├── LICENSE                     # Apache 2.0 license
├── requirements.txt            # Python dependencies
├── .env.example               # Configuration template
├── scripts/
│   ├── pay_later.py           # Core payment functions
│   ├── config.py              # Configuration management
│   ├── create_payment.py       # Payment creation examples
│   └── webhook_handler.py      # Stripe webhook handler
└── references/
    ├── payment_methods.md      # Payment method details
    └── integration_guide.md    # Complete setup guide
```

## Core Functions

### Create a Payment

```python
from scripts.pay_later import create_pay_later_payment

payment = create_pay_later_payment(
    amount=10000,  # $100.00 in cents
    currency="usd",
    payment_method="afterpay_pay_now",
    customer_email="customer@example.com",
    description="Product purchase"
)
```

### Confirm Payment

```python
from scripts.pay_later import confirm_payment

confirmation = confirm_payment(payment['id'])
print(f"Status: {confirmation['status']}")
```

### Get Payment Methods

```python
from scripts.pay_later import get_payment_methods

methods = get_payment_methods(customer_id="cus_...")
```

## Configuration

See [integration_guide.md](references/integration_guide.md) for complete setup instructions.

**Environment Variables:**
- `STRIPE_API_KEY` - Your Stripe secret key
- `STRIPE_PUBLISHABLE_KEY` - Your Stripe publishable key
- `STRIPE_WEBHOOK_SECRET` - Webhook signing secret
- `STRIPE_CURRENCY` - Default currency (default: usd)
- `STRIPE_RETURN_URL` - Post-payment redirect URL

## Security

⚠️ **Important Security Notes:**
- Never commit `.env` file with real API keys
- Use environment variables in production
- Always verify webhook signatures
- Implement HTTPS for webhook endpoints
- Keep Stripe library updated

## Documentation

- **[SKILL.md](SKILL.md)** - Agent Skills specification and API
- **[Integration Guide](references/integration_guide.md)** - Complete setup instructions
- **[Payment Methods](references/payment_methods.md)** - Details on each payment option

## Examples

See `scripts/` directory for complete working examples:
- `create_payment.py` - Creating Afterpay and Klarna payments
- `webhook_handler.py` - Processing Stripe events
- `config.py` - Configuration management

## Support

For help with:
- **Setup issues** - See [Integration Guide](references/integration_guide.md)
- **Payment methods** - See [Payment Methods](references/payment_methods.md)
- **Stripe API** - Visit [Stripe Docs](https://stripe.com/docs)
- **Errors** - Check [Stripe Error Codes](https://stripe.com/docs/error-codes)

## License

Apache License 2.0 - See [LICENSE](LICENSE)
