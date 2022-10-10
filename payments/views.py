from django.urls.base import reverse
from django.views.generic.list import ListView
import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect, render, HttpResponse
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from stripe.api_resources.checkout import session
from events.models import EventModel
# from accounts.models import User
from payments.models import EventBuy, UserRole
from accounts.models import  User

stripe.api_key=settings.STRIPE_SECRET_KEY



class SuccessView(TemplateView):
    template_name="payments/success.html"
class CancelView(TemplateView):
    template_name="payments/cancellation.html"


class LandingView(TemplateView):
    template_name = "payments/landing.html"

    def get_context_data(self, **kwargs):
        product = EventBuy.objects.get(id=self.kwargs['pk'])
        context = super(LandingView, self).get_context_data(**kwargs)
        context.update({
            "product": product,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        event=EventModel.objects.get(title=product.name)

        context['event'] = event
        return context


class PaymentListView(ListView):
    model=EventBuy
    template_name="payments/list.html"
    paginate_by=9
    def get_queryset(self):
        page_obj=EventBuy.objects.order_by('name')
        return page_obj

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        if request.user.get_role_display() is not "follower":
            product_id = self.kwargs["pk"]
            print("this is the request"+str(request.user.id))
            product = EventBuy.objects.get(id=product_id)
            YOUR_DOMAIN = "http://127.0.0.1:8000"
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'sek',
                            'unit_amount': product.price,
                            'product_data': {
                                'name': product.name,
                                # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    "product_id": product.id,
                    "user_id":request.user.id
                },
                # the_user=request.user,
                mode='payment',
                success_url=YOUR_DOMAIN + '/payment/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
            return JsonResponse({
                'id': checkout_session.id
            })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
    # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    # Invalid signature
        return HttpResponse(status=400)
      # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        customer_email= session["customer_details"]["email"]
        product_id=session["metadata"]["product_id"]
        the_user=User.objects.get(id=session["metadata"]["user_id"])
        print("the user id is" + str(session["metadata"]["user_id"]))
        product= EventBuy.objects.get(id=product_id)
        userrole=UserRole(event=product, user=the_user)
        userrole.save()
        send_mail(
            subject="here is your invitation number",
            message="Thanks for joining the event, the reference number is  "+userrole.referrence_number+" .",
            recipient_list=[customer_email],
            from_email="donotreply@example.com",
        )


    # Passed signature verification
    return HttpResponse(status=200)
