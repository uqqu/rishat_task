import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from .models import Discount, Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class OrderView(View):
    '''Get order (or order with one item) page'''

    def get(self, request, pk, order):
        if order:
            order = Order.objects.get(pk=pk)
        else:
            item = Item.objects.get(pk=pk)
            order = Order()
            order.save()
            order.items.add(item)
        return render(
            request,
            'stripe_api/order.html',
            {'order': order, 'stripe_pk': settings.STRIPE_PUBLIC_KEY},
        )


class CreateCheckoutSessionView(View):
    '''Get Stripe session.id to redirect to checkout.stripe.com'''

    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        items = []
        for item in order.items.all():
            items.append(
                {
                    'quantity': 1,
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item.price,
                        'product_data': {'name': item.name, 'description': item.description},
                        'tax_behavior': 'exclusive',
                    },
                }
            )
            if item.tax:
                items[-1]['price_data']['product_data']['tax_code'] = 'txcd_' + item.tax.code
        discounts = []
        if order.discount:
            discounts.append({'coupon': order.discount.coupon_id})
        checkout_session = stripe.checkout.Session.create(
            success_url='http://127.0.0.1:8000/success',
            cancel_url='http://127.0.0.1:8000/failed',
            mode='payment',
            line_items=items,
            automatic_tax={'enabled': True},
            discounts=discounts,
        )
        return JsonResponse({'id': checkout_session.id})


class CreateCouponView(View):
    '''Create new fixed-percent coupon'''

    def get(self, request):
        coupon = stripe.Coupon.create(percent_off=20, duration='once')
        Discount.objects.create(pk=coupon.id)
        return redirect('admin/')
