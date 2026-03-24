import stripe
from django.conf import settings
from decouple import config, UndefinedValueError

def get_stripe_api_key():
    """Attempt to get the Stripe API key from environment or settings."""
    try:
        # Try to load from environment variable
        return config('STRIPE_SECRET_KEY_TEST')
    except UndefinedValueError:
        try:
            # Fallback to Django settings
            return settings.STRIPE_SECRET_KEY_TEST
        except AttributeError:
            print("Error: STRIPE_SECRET_KEY_TEST not found in environment variables or Django settings.")
            print("Please set STRIPE_SECRET_KEY_TEST in your .env file or settings.py.")
            print("You can find your API key in the Stripe Dashboard: https://dashboard.stripe.com/test/apikeys")
            return None

def list_alternative_prices():
    """List active prices from Stripe as alternatives for invalid price IDs."""
    try:
        prices = stripe.Price.list(active=True, limit=10)  # Limit to 10 for brevity
        if prices.data:
            print("\nAvailable active prices in your Stripe account:")
            for price in prices.data:
                print(f"- Price ID: {price.id}, Product: {price.product}, Amount: {price.unit_amount / 100:.2f} {price.currency}")
        else:
            print("\nNo active prices found in your Stripe account.")
    except stripe.error.StripeError as e:
        print(f"Error listing alternative prices: {str(e)}")

def check_price_ids():
    # Configure Stripe API key
    stripe.api_key = get_stripe_api_key()
    if not stripe.api_key:
        print("Cannot proceed without a valid Stripe API key.")
        return

    # Define the subscription price IDs (same as in your views.py)
    subscription = {
        'basic': 'price_1RgsVTAWdYwu0IZpibyhhifl',
        'pro': 'price_1RgsYqAWdYwu0IZpwfXBFQf4',
        'premium': 'price_1RgsazAWdYwu0IZpqGNQ7fnZ',
    }

    # Test API key validity with a simple call
    try:
        stripe.Price.list(limit=1)  # Minimal API call to verify key
        print("Stripe API key is valid.")
    except stripe.error.AuthenticationError as e:
        print(f"Invalid Stripe API key: {str(e)}")
        print("Please verify your STRIPE_SECRET_KEY_TEST in the Stripe Dashboard: https://dashboard.stripe.com/test/apikeys")
        return
    except stripe.error.StripeError as e:
        print(f"Error connecting to Stripe: {str(e)}")
        return

    # Check each price ID
    invalid_prices = False
    for plan, price_id in subscription.items():
        try:
            # Attempt to retrieve the price from Stripe
            price = stripe.Price.retrieve(price_id)
            if price.active:
                print(f"Price ID for '{plan}' ({price_id}) is VALID and ACTIVE.")
            else:
                print(f"Price ID for '{plan}' ({price_id}) is VALID but INACTIVE.")
        except stripe.error.InvalidRequestError as e:
            print(f"Price ID for '{plan}' ({price_id}) is INVALID: {str(e)}")
            invalid_prices = True
        except stripe.error.StripeError as e:
            print(f"Error checking price ID for '{plan}' ({price_id}): {str(e)}")

    # If any price IDs are invalid, suggest alternatives
    if invalid_prices:
        print("\nSome price IDs are invalid. Fetching alternative price IDs from your Stripe account...")
        list_alternative_prices()

if __name__ == "__main__":
    check_price_ids()