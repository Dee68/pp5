from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = models.CharField(max_length=8, unique=True)
    email = models.EmailField(_('email address'), unique=True, max_length=20)
    is_email_verified = models.BooleanField(default=False)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return str(self.username)


class Profile(models.Model):
    """User profile to extend the account profile
    Added images so they can be displayed on the blog if users comment.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    street_address1 = models.CharField(blank=True, max_length=100, null=True)
    street_address2 = models.CharField(blank=True, default=00, max_length=100)
    town_or_city = models.CharField(blank=True, max_length=30)
    county = models.CharField(blank=True, default=00, max_length=30, null=True)
    postcode = models.CharField(blank=True, max_length=30)
    country = CountryField(blank=True, max_length=30)
    avatar = models.ImageField(blank=True, upload_to='profile_pics/')

    def image_tag(self):
        if self.avatar:
            return mark_safe(
                '<img src="%s" height="50" width="50">' % self.avatar.url
                )
        return "No image found"

    def __str__(self):
        return self.user.username

    def full_address(self):
        return f'(self.street_address1) (self.street_address2)'
