# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.test import TestCase
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Internal:
from account.models import Profile
from shop.models import Product, Review, Category
from checkout.models import Order
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This tests check the creation, update of the product


class BaseTest(TestCase):
    def setUp(self):
        self.home_url = reverse('home:home')
        self.register_url = reverse('account:register')
        self.login_url = reverse('account:signin')
        self.logout_url = reverse('account:logout')
        self.add_review_url = reverse('shop:add_review', kwargs={'pk': 1})
        self.review_url = reverse('account:reviews')
        self.category = {
                'id': 1,
                'name': 'coverlocker',
                'slug': 'coverlocker',
                'friendly_name': '',
                'description': ''
        }
        self.product = {
            'id': 1,
            'name': '',
            'slug': '',
            'description': '',
            'price': 5.00,
            'in_stock': True,
            'has_sizes': False,
            'category': 1,
            'rating': 5,
            'image_url': '',
            'image': 'image'
        }
        self.user = {
            'username': 'username',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        self.user_bad_name = {
            'username': '1abc',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        self.user_with_empty_name = {
            'username': '',
            'email': 'noreply@gmail.com',
            'password1': '',
            'password2': 'password'
        }
        self.user_with_short_name = {
            'username': 'u',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        self.user_with_long_name = {
            'username': 'usernameusername12345',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        self.user_with_non_alphanumeric = {
            'username': 'user@12',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        self.user_with_no_match_password = {
            'username': 'user',
            'email': 'noreply@gmail.com',
            'password1': 'password1',
            'password2': 'password2'
        }
        self.user_with_invalid_email = {
            'username': 'user',
            'email': 'noreply@com',
            'password1': 'password',
            'password2': 'password'
        }
        self.user_with_taken_email = {
            'username': 'test',
            'email': 'noreply@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        self.user_with_taken_name = {
            'username': 'username',
            'email': 'noreply1@gmail.com',
            'password1': 'password',
            'password2': 'password'
        }
        self.user_empty_login = {
            'username': '',
            'password': ''
        }

        return super().setUp()


class Producttest(BaseTest):
    pass
