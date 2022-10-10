from django.contrib.auth.mixins import AccessMixin
from accounts.models import User
from django.shortcuts import redirect, render
from django.urls.base import reverse, reverse_lazy
from django.views.generic import View,UpdateView
from django.contrib.auth import authenticate ,login,logout
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import logout

from accounts.models import User
from .forms import CustomUserCreationForm,LoginForm, SubscriberForm, UserChangeForm, UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage, message
import threading
from django.contrib import messages

class EmailThread(threading.Thread):

    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send()

class UserRequiredMixin:
    user_field = 'email'

    def get_queryset(self):
        return super().get_queryset().filter(
            **{self.user_field: self.request.user.email}
    )

# class UserFilterViewMixin:
#     user_field = 'user'

#     def get_queryset(self):
#         return super().get_queryset().filter(
#             **{self.user_field: self.request.user}
#     )
def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('accounts/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )
    EmailThread(email).start()

def logout_view(request):
    logout(request)
    return redirect('home:home')

def signup_page(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role="FOLLOWER"
            user.is_active = True
            user.save()

            send_activation_email(user,request)
            print("send the email to verification")
            messages.add_message(request, messages.SUCCESS,
                                 'We sent you an email to verify your account')
            return redirect('/accounts/login/')
            # return render(request, 'accounts/login.html', context={'message':message})
    return render(request, 'accounts/signup.html', context={'form': form})



class LoginPageView(View):
    template_name = 'authentication/login.html'
    form_class = LoginForm
    
    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user and not user.is_email_verified:
                messages.add_message(request, messages.ERROR,
                                 'Email is not verified, please check your email inbox')
                print ("in Email Is not verified")
                return render(request, self.template_name, context={'form': form})
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.ERROR,
                                 'login succesfully')
                return redirect('/')
            messages.add_message(request, messages.ERROR,
                                 'Invalid credentials, try again')   
            
        return render(request, self.template_name, context={'form': form,})


# def logout_user(request):

#     logout(request)

#     messages.add_message(request, messages.SUCCESS,
#                          'Successfully logged out')

#     return redirect(reverse('login'))


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('accounts:login')


def activate_user(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('accounts:login'))

    return render(request, 'accounts/activate-failed.html', {"user": user})



class SubscribingView(UserRequiredMixin,UpdateView):
    model=User
    form_class=SubscriberForm
    template_name="accounts/create-sub.html"
    success_url="/"
    def post(self, request, **kwargs):
    # "first_name","last_name","phone_no", "profile_photo","id"
        request.POST = request.POST.copy()
        self.object = self.get_object()
        request.POST['first_name'] = self.object.first_name
        request.POST['last_name'] = self.object.last_name
        request.POST['phone_no'] = self.object.phone_no
        request.POST['profile_photo'] = self.object.profile_photo
        # if request.POST['first_name'] and request.POST['last_name']  and request.POST['phone_no']  is not None:
        if request.user.get_role_display() is "follower":
            request.user.role = User.SUBSCRIBER
            request.user.save()
        
        return super(SubscribingView, self).post(request, **kwargs)
    
