#!/usr/bin/env python3
"""
Stripe Pay Later - Setup Verification Script

Run this script to verify your Stripe configuration is correct.
Usage: python verify_setup.py
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if required environment variables are set"""
    print("=" * 60)
    print("ENVIRONMENT VARIABLES CHECK")
    print("=" * 60)
    
    required_vars = ["STRIPE_API_KEY", "STRIPE_PUBLISHABLE_KEY"]
    optional_vars = ["STRIPE_WEBHOOK_SECRET", "STRIPE_CURRENCY"]
    
    all_good = True
    
    for var in required_vars:
        if var in os.environ:
            value = os.environ[var]
            masked = value[:20] + "..." if len(value) > 20 else value
            print(f"✓ {var}: {masked}")
        else:
            print(f"✗ {var}: NOT SET (REQUIRED)")
            all_good = False
    
    for var in optional_vars:
        if var in os.environ:
            print(f"✓ {var}: {os.environ[var]}")
        else:
            print(f"- {var}: not set (optional)")
    
    return all_good


def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n" + "=" * 60)
    print("DEPENDENCIES CHECK")
    print("=" * 60)
    
    dependencies = {
        "stripe": "stripe>=7.0.0",
        "flask": "flask>=2.0.0 (optional, for webhooks)",
        "requests": "requests>=2.25.0",
    }
    
    all_good = True
    
    for module, version_info in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {module}: {version_info}")
        except ImportError:
            print(f"✗ {module}: NOT INSTALLED - {version_info}")
            all_good = False
    
    return all_good


def test_stripe_connection():
    """Test connection to Stripe API"""
    print("\n" + "=" * 60)
    print("STRIPE API CONNECTION TEST")
    print("=" * 60)
    
    try:
        import stripe
        
        api_key = os.environ.get("STRIPE_API_KEY")
        if not api_key:
            print("✗ STRIPE_API_KEY not set")
            return False
        
        stripe.api_key = api_key
        
        # Try to list customers (no sensitive data, just connectivity test)
        try:
            stripe.Customer.list(limit=1)
            print("✓ Successfully connected to Stripe API")
            
            # Get account info
            try:
                account = stripe.Account.retrieve()
                print(f"✓ Account email: {account.get('email', 'N/A')}")
                print(f"✓ Account country: {account.get('country', 'N/A')}")
            except Exception as e:
                print(f"⚠ Could not retrieve account details: {str(e)}")
            
            return True
        except stripe.error.AuthenticationError:
            print("✗ Invalid API key - authentication failed")
            return False
        except stripe.error.StripeError as e:
            print(f"✗ Stripe API error: {str(e)}")
            return False
    except ImportError:
        print("✗ stripe package not installed")
        return False


def check_file_structure():
    """Check if all required files exist"""
    print("\n" + "=" * 60)
    print("FILE STRUCTURE CHECK")
    print("=" * 60)
    
    base_path = Path(__file__).parent
    required_files = [
        "SKILL.md",
        "requirements.txt",
        "README.md",
        ".env.example",
        "scripts/pay_later.py",
        "scripts/config.py",
    ]
    
    all_good = True
    
    for file in required_files:
        file_path = base_path / file
        if file_path.exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file}: NOT FOUND")
            all_good = False
    
    return all_good


def test_imports():
    """Test if modules can be imported"""
    print("\n" + "=" * 60)
    print("IMPORT TEST")
    print("=" * 60)
    
    all_good = True
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / "scripts"))
        import pay_later
        print("✓ pay_later module imports successfully")
    except Exception as e:
        print(f"✗ Failed to import pay_later: {str(e)}")
        all_good = False
    
    try:
        import config
        print("✓ config module imports successfully")
    except Exception as e:
        print(f"✗ Failed to import config: {str(e)}")
        all_good = False
    
    return all_good


def main():
    """Run all checks"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "STRIPE PAY LATER SETUP VERIFICATION" + " " * 9 + "║")
    print("╚" + "=" * 58 + "╝")
    
    checks = [
        ("Environment Variables", check_environment),
        ("File Structure", check_file_structure),
        ("Dependencies", check_dependencies),
        ("Module Imports", test_imports),
        ("Stripe API Connection", test_stripe_connection),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n✗ Error during {check_name}: {str(e)}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {check_name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Your Stripe Pay Later setup is ready.")
        print("\nNext steps:")
        print("1. Review the integration guide: references/integration_guide.md")
        print("2. Try creating a test payment: python scripts/create_payment.py")
        print("3. Set up webhooks for production")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please review the issues above.")
        print("\nCommon solutions:")
        print("- Set STRIPE_API_KEY: export STRIPE_API_KEY='sk_test_...'")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Check file paths are correct")
        return 1


if __name__ == "__main__":
    sys.exit(main())
