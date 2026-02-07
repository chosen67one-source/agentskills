# Pay Later Payment Methods Reference

## Afterpay

**What is it?**
Afterpay is a buy-now-pay-later service that allows customers to split their purchases into 4 interest-free payments every 2 weeks.

**Key Features:**
- 4 equal installments spread over 8 weeks
- No interest or fees (if paid on time)
- Instant approval for most transactions
- Works with merchants in US, UK, and other regions

**Integration Details:**
- Payment method type: `afterpay_pay_now`
- Minimum transaction: $35 (varies by region)
- Maximum transaction: $2,000 (varies by region)
- Automatic reminders and collections

**Customer Experience:**
1. Customer selects Afterpay at checkout
2. Redirected to Afterpay for authorization
3. Immediate payment capture initiated
4. Customer receives payment schedule

**Webhook Events:**
- `payment_intent.succeeded` - Payment approved
- `payment_intent.payment_failed` - Payment rejected
- `charge.refunded` - Refund initiated

---

## Klarna

**What is it?**
Klarna is a global payments service offering multiple payment options including pay later and installment plans.

**Key Features:**
- Multiple pay later options (Split in 2, Pay in 4, Monthly plans)
- Pay in 30 days option
- Up to 12-month installment plans available
- Available in many countries (US, EU, UK, etc.)

**Integration Details:**
- Payment method type: `klarna`
- More flexible amount limits than Afterpay
- Regional variations in payment options

**Payment Options:**
1. **Pay Later** - Pay in 30 days
2. **Pay in 4** - 4 interest-free payments
3. **Pay Over Time** - Flexible longer-term plans
4. **Financing** - Credit-based financing

**Assessment Process:**
- Soft credit check (typically no impact on credit score)
- Instant decision for most customers
- Seamless integration with checkout flow

---

## PayPal

**What is it?**
PayPal's payment solutions including PayPal Credit (BNPL) and standard payments.

**Key Features:**
- Established payment method trusted by consumers
- PayPal Credit for eligible purchases
- Wallet functionality across merchants
- Buyer protection

**Integration Details:**
- Payment method type: `paypal`
- Works with PayPal's existing merchant relationships
- Standard payment processing plus BNPL options

---

## Card Payments

**What is it?**
Traditional credit and debit card processing with optional installment support.

**Key Features:**
- Standard Visa, Mastercard, American Express, Discover
- 3D Secure authentication available
- Tokenization for future payments
- Integration with various card networks

**Integration Details:**
- Payment method type: `card`
- Industry standard security measures
- Wide acceptance globally

**Card Types Supported:**
- Visa
- Mastercard
- American Express
- Discover
- Diners Club
- JCB

---

## Comparison Matrix

| Feature | Afterpay | Klarna | PayPal | Card |
|---------|----------|--------|--------|------|
| Interest-Free | Yes | Yes* | Varies | No |
| Installments | 4 x 2 weeks | 2-12x | Varies | No |
| Instant Decision | Yes | Yes | Varies | Quick |
| Global Support | Limited | Wide | Wide | Universal |
| Min Amount | $35 | Varies | None | None |
| Max Amount | $2,000 | Higher | None | Varies |

*Klarna conditions apply

---

## Regional Availability

### Afterpay
- United States ✓
- United Kingdom ✓
- Australia ✓
- New Zealand ✓
- Canada ✓
- France ✓
- Spain ✓
- Italy ✓

### Klarna
- United States ✓
- United Kingdom ✓
- Sweden ✓
- Germany ✓
- Netherlands ✓
- Austria ✓
- Spain ✓
- Italy ✓
- France ✓
- Belgium ✓
- Portugal ✓
- Ireland ✓
- Finland ✓
- Denmark ✓
- Norway ✓

### PayPal
- All major countries ✓

### Card Payments
- Global ✓
