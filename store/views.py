from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from carts.models import CartItem
from carts.views import cart_id

from .models import Product, Category


# Create your views here.

def store(request, category_slug=None):
  if category_slug != None:
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
      category=category, is_available=True).order_by('id')
    product_count = products.count()
  else:
    products = Product.objects.filter(is_available=True)
    product_count = products.count()
  
  paginator = Paginator(products, 6)
  page = request.GET.get('page')
  paged_products = paginator.get_page(page)

  context = {
      'products': paged_products,
      'product_count': product_count
  }
  return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
  try:
    product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    in_cart = CartItem.objects.filter(cart__cart_id=cart_id(request), product=product).exists()
  except Exception as e:
    raise e
  
  context = { 'product' : product, 'in_cart': in_cart, }
  return render(request, 'store/product_detail.html', context)


def search(request):
  keyword = request.GET.get('keyword', None)
  if keyword:
    products = Product.objects.order_by('-created_at').filter(
      Q(description__icontains=keyword) | Q(name__icontains=keyword))
  context = {
      'products': products,
      'product_count': products.count()
  }
  return render(request, 'store/store.html', context=context)
