from django.urls import path

from .views import CreateCheckoutSessionView, CreateCouponView, OrderView

urlpatterns = [
    path('item/<int:pk>', OrderView.as_view(), {'order': False}),
    path('order/<int:pk>', OrderView.as_view(), {'order': True}),
    path('buy/<int:pk>', CreateCheckoutSessionView.as_view()),
    path('create_coupon', CreateCouponView.as_view()),
]
