from django.db import models
from django.urls import reverse 


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True) # blank because it's optional
    image = models.ImageField(upload_to='photos/categories/', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category_slug', args=[self.slug])

    def __str__(self):
        return self.name
