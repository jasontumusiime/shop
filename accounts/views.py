from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm
from .models import Account
from carts.models import Cart, CartItem
from carts.views import cart_id


def register(request):
  if request.method == 'POST':

    form = RegistrationForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      email = form.cleaned_data['email']
      phone_number = form.cleaned_data['phone_number']
      password = form.cleaned_data['password']
      username = email.split('@')[0]
      user = Account.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        username=username
      )
      user.phone_number = phone_number
      user.save()

      # User Activation
      current_site = get_current_site(request)
      mail_subject = "Please activate your site"
      message = render_to_string('accounts/account_verification_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
      })
      to_email = email
      mailer = EmailMessage(mail_subject, message, to=[to_email])
      mailer.send()

      # messages.success(request, "Registration successful!")
      return redirect(f'/accounts/login/?command=verification&email={email}')
  else:
    form = RegistrationForm

  context = { 'form': form,}
  return render(request, 'accounts/register.html', context)

# TODO: Remove business login out of controllers
def login(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']

    user = auth.authenticate(email=email, password=password)
    if user is not None:
      try:
        cart = Cart.objects.get(cart_id=cart_id(request))
        anon_cart_items = CartItem.objects.filter(cart=cart)
        if anon_cart_items.exists():

          anon_variations, anon_items = [], {}
          for item in anon_cart_items:
            anon_variations.append(list(item.variations.all()))
            anon_items[item.id] = item

          existn_varitions, existn_item_ids = [], []
          existn_cart_items = CartItem.objects.filter(user=user)
          for item in existn_cart_items:
            existn_varitions.append(list(item.variations.all()))
            existn_item_ids.append(item.id)

          for variation in anon_variations:
            if variation in existn_varitions:
              index = existn_varitions.index(variation)
              item_id = existn_item_ids[index]
              item = CartItem.objects.get(id=item_id)
              item.quantity += 1
            else:
              index = anon_variations.index(variation)
              item = anon_items[index]

            item.user = user
            item.save()
              
      except Exception as e:
        raise e
      
      auth.login(request, user)
      messages.success(request, "Successfully loggedin!")
      return redirect('dashboard')
    else:
      messages.error(request, "Invalid login credentials!")
      return redirect('login')
  return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
  auth.logout(request)
  messages.success(request, "You are logged out!")
  return redirect('login')


def activate(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64)
    user = Account.objects.get(pk=uid)
  except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
    user = None

  if user and default_token_generator.check_token(user, token):
    user.is_active = True
    user.save()
    messages.success(request, "You account has been successfully activated!")
    return redirect('login')
  else:
    messages.error(request, 'Invalid activation link')
    return redirect('register')
  

@login_required(login_url= 'login')
def dashboard(request):
  return render(request, 'accounts/dashboard.html')


def forgotPassword(request):
  if request.method == 'POST':
    
    email = request.POST['email']
    if Account.objects.filter(email=email).exists():
      user = Account.objects.get(email__exact=email)
      print('User ID: ' + str(user.pk))
      # Password Recovery
      current_site = get_current_site(request)
      mail_subject = "Reset your password"
      message = render_to_string('accounts/reset_password_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
      })
      to_email = email
      mailer = EmailMessage(mail_subject, message, to=[to_email])
      mailer.send()

      messages.success(request, 'Password reset email has been sent your email')
      return redirect('login')
  
    else:
      messages.error(request, "Account does not exist")
      return redirect('forgotPassword')

  return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
  try:
    uid = urlsafe_base64_decode(uidb64)
    user = Account.objects.get(pk=uid)
  except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
    user = None

  if user and default_token_generator.check_token(user, token):
    request.session['uid'] = uid
    messages.success(request, "Please reset your password")
    return redirect('resetPassword')
  else:
    messages.error(request, 'This link has been expired')
    return redirect('login')
  

def resetPassword(request):
  if request.method == 'POST':
    password = request.POST['password']
    re_password = request.POST['cofirm_password']

    if re_password == password:
      uid = request.session.get('uid')
      user = Account.objects.get(pk=uid)
      user.set_password(password)
      user.save()

      messages.success(request, 'Password reset successful')
      return redirect('login')
    else:
      messages.error(request, "Passwords do not match")
      return redirect('resetPassword')
    
  return render(request, 'accounts/resetPassword.html')