from django.db import models
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=250, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('shop:products_by_category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='products/')
    rating = models.FloatField(null=True)

    def image_tag(self):
        if self.image:
            return mark_safe(
                    '<img src="%s" height="50" width="50">' % self.image.url)
        return "No image found"

    def get_absolute_url(self):
        return reverse(
            'shop:product_detail',
            args=[self.category.slug, self.slug]
            )

    def __str__(self):
        return self.name


class Rating(models.Model):
    rating = models.SmallIntegerField()

    def __str__(self):
        return str(self.rating)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(
                             settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE
                             )
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    review = models.TextField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s review on {self.product.name}"
