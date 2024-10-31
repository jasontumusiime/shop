from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from store.models import Product, Variation

from . models import Cart, CartItem

# Create your views here.

from django.http import HttpResponse


def cart_id(request):
  cart = request.session.session_key
  if not cart:
    cart = request.session.create()
  return cart


def add_cart(request, product_id):

  product = Product.objects.get(id=product_id)
  current_user = request.user
  if current_user.is_authenticated:
    # if user is authenticated
    product_vars = []
    if request.method == 'POST':
      for var_category in request.POST:
        var_value = request.POST[var_category]
        try:
          variation = Variation.objects.get(
            product__id=product_id, 
            category__iexact=var_category, 
            value__iexact=var_value
          )
          product_vars.append(variation)
        except:
          pass

    cart_item = CartItem.objects.filter(product=product, user=current_user)
    if cart_item.exists():
      ex_var_list, ids = [], []
      for item in cart_item:
        ex_var_list.append(list(item.variations.all()))
        ids.append(item.id)
      
      if product_vars in ex_var_list:
        index = ex_var_list.index(product_vars)
        item_id = ids[index]
        item = CartItem.objects.get(product=product, id=item_id)
        item.quantity += 1
        item.save()
        
      else:
        item = CartItem.objects.create(product=product, quantity=1, user=current_user)
        if len(product_vars) > 0:
          item.variations.clear()
          item.variations.add(*product_vars)
        item.save()
    else:
      cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
      if len(product_vars) > 0:
        cart_item.variations.clear()
        cart_item.variations.add(*product_vars)
      cart_item.save()
  else:
    product_vars = []
    if request.method == 'POST':
      for var_category in request.POST:
        var_value = request.POST[var_category]
        print(f"{var_category} + ' ' + {var_value}")

        try:
          variation = Variation.objects.get(
            product__id=product_id, 
            category__iexact=var_category, 
            value__iexact=var_value
          )
          product_vars.append(variation)
        except:
          pass
    try:
      cart = Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist as e:
      cart = Cart.objects.create(cart_id=cart_id(request))
      cart.save()

    cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if cart_item_exists:
      cart_item = CartItem.objects.filter(product=product, cart=cart)

      ex_var_list, ids = [], []
      for item in cart_item:
        ex_var_list.append(list(item.variations.all()))
        ids.append(item.id)
      
      if product_vars in ex_var_list:
        index = ex_var_list.index(product_vars)
        item_id = ids[index]
        item = CartItem.objects.get(product=product, id=item_id)
        item.quantity += 1
        item.save()
        
      else:
        item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if len(product_vars) > 0:
          item.variations.clear()
          item.variations.add(*product_vars)
        item.save()
    else:
      cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
      if len(product_vars) > 0:
        cart_item.variations.clear()
        cart_item.variations.add(*product_vars)
      cart_item.save()

  return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
  try:
    tax = grand_total = 0
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(user=request.user)
    else:
      cart = Cart.objects.get(cart_id=cart_id(request))
      cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    for item in cart_items:
      total += item.product.price * item.quantity
      quantity += item.quantity
    tax = (2 / 100) * total
    grand_total = total + tax
  except ObjectDoesNotExist:
    pass

  context = { 
    'total': total, 
    'quantity': quantity, 
    'cart_items': cart_items, 
    'grand_total': grand_total,
    'tax': tax,
  }
  return render(request, 'store/cart.html', context)


def remove_cart(request, product_id, cart_item_id):
  product = get_object_or_404(Product, id=product_id)
  try:
    if request.user.is_authenticated:
      cart_item = CartItem.objects.get(product, user=request.user, id=cart_item_id)
    else:
      cart = Cart.objects.get(cart_id=cart_id(request))
      cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_item_id)
    
    if cart_item.quantity <= 1:
      cart_item.delete()
    else:
      cart_item.quantity -= 1
      cart_item.save()
  except:
    pass  
  return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
  product = get_object_or_404(Product, id=product_id)
  if request.user.is_authenticated:
    cart_item = CartItem.objects.get(user=request.user, product=product, id=cart_item_id)
  else:
    cart = Cart.objects.get(cart_id=cart_id(request))
    cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_item_id)
  cart_item.delete()
  return redirect('cart')

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
  try:
    tax = grand_total = 0
    cart = Cart.objects.get(cart_id=cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    for item in cart_items:
      total += item.product.price * item.quantity
      quantity += item.quantity
    tax = (2 / 100) * total
    grand_total = total + tax
  except ObjectDoesNotExist:
    pass

  context = { 
    'total': total, 
    'quantity': quantity, 
    'cart_items': cart_items, 
    'grand_total': grand_total,
    'tax': tax,
  }
  return render(request, 'store/checkout.html', context)
