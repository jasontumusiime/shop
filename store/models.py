from django.db import models
from django.urls import reverse

from category.models import Category

# Create your models here.
class Product(models.Model):
  name          = models.CharField(max_length=200, unique=True)
  slug          = models.CharField(max_length=200, unique=True)
  description   = models.TextField(max_length=500, blank=True)
  price         = models.IntegerField()
  image         = models.ImageField(upload_to='photos/products', blank=True)
  stock         = models.IntegerField()
  is_available  = models.BooleanField(default=True)
  category      = models.ForeignKey(Category, on_delete=models.CASCADE)
  created_at    = models.DateTimeField(auto_now_add=True)
  modified_at   = models.DateTimeField(auto_now=True)

  def get_url(self):
    return reverse('product_detail', args=[self.category.slug, self.slug])

  def __str__(self):
    return self.name
  

class VariationManager(models.Manager):
  def colors(self):
    return super().filter(category='color', is_active=True)

  def sizes(self):
    return super().filter(category='size', is_active=True)


class Variation(models.Model):
  variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
  )

  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  category = models.CharField(max_length=100, choices=variation_category_choice) 
  value = models.CharField(max_length=100)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)

  objects = VariationManager()

  def __str__(self):
    return str(self.value)