from django.core.exceptions import ObjectDoesNotExist

from .models import Cart, CartItem
from .views import cart_id


def counter(request):
  if 'admin' in request.path:
    return {}
  else:
    try:
      cart = Cart.objects.get(cart_id=cart_id(request))
      cart_items = CartItem.objects.filter(cart=cart)
      cart_count = sum(item.quantity for item in cart_items)
    except ObjectDoesNotExist:
      cart_count = 0
    return {'cart_count': cart_count} 
