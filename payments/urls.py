from os import name
from django.contrib import admin
from django.urls import path

from payments.views import (
    CancelView,
    CreateCheckoutSessionView,
    LandingView,
    SuccessView,
    PaymentListView,
    stripe_webhook
)

app_name='payment'
urlpatterns = [
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(),name='create-checkout-session'),
    path('',PaymentListView.as_view(),name='payment_list' ),
    path('<pk>/', LandingView.as_view(),name='landing-page'),
    path('cancel/', CancelView.as_view(), name="cancel"),
    path('success/', SuccessView.as_view(), name='success'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
]