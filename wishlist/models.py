from django.db import models
from shop.models import Product
from account.models import CustomUser
from django.conf import settings


class Wishlist(models.Model):
    user = models.ForeignKey(
                             settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE
                             )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} whish list'
