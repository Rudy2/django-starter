from django.shortcuts import render, redirect, reverse
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY_TEST

def subscription_view(request):
    subscription = {
        'basic': 'price_1RgsVTAWdYwu0IZpibyhhifl',
        'pro': 'price_1RgsYqAWdYwu0IZpwfXBFQf4',
        'premium': 'price_1RgsazAWdYwu0IZpqGNQ7fnZ',
    }

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"{reverse('account_login')}?next={request.get_full_path()}")

        price_id = request.POST.get('price_id')

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            payment_method_types=['card'],
            mode='subscription',
            success_url= request.build_absolute_uri(reverse("create_subscription")) + f'?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=request.build_absolute_uri(f'{reverse("subscription")}'),
            customer_email=request.user.email,
            metadata={
                'user_id': request.user.id,
            }

        )
        return redirect(checkout_session.url, code=303)

    return render(request, 'a_subscription/subscriptions.html', {'subscriptions': subscription})

def create_subscription(request):
    checkout_session_id = request.GET.get('session_id', None)

    # creat subscription object in database
    return redirect('my_sub')

def my_sub_view(request):
    return render(request, 'a_subscription/my-sub.html')
