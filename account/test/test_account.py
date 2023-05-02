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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This tests check the creation, update of the user profile


class BaseTest(TestCase):
    def setUp(self):
        self.home_url = reverse('home:home')
        self.register_url = reverse('account:register')
        self.login_url = reverse('account:signin')
        self.logout_url = reverse('account:logout')
        self.profile_url = reverse('account:profile')
        self.profile = {
            'street_address1': '',
            'street_address2': '',
            'town_or_city': '',
            'county': '',
            'postcode': '',
            'country': '',
            'address': 'abc 123',
            'avatar': ''
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


class RegisterTest(BaseTest):
    def test_show_register_page(self):
        response = self.client.get(self.register_url)
        self.assertTemplateUsed(response, 'account/register.html')
        self.assertEqual(response.status_code, 200)

    def test_can_create_user(self):
        response = self.client.post(
                                    self.register_url,
                                    self.user,
                                    format='text/html'
                                    )
        message = "Account created successfully.\
                   Check your mail to activate\
                   account."
        self.user['is_active'] = True
        self.assertEquals(response.status_code, 200,  msg=message)

    def test_can_not_register_user_with_empty_username(self):
        response = self.client.post(
                                    self.register_url,
                                    self.user_with_empty_name,
                                    format='text/html'
                                    )
        self.assertEqual(response.status_code, 400)

    def test_can_not_register_user_with_short_username(self):
        response = self.client.post(
                                    self.register_url,
                                    self.user_with_short_name,
                                    format='text/html'
                                    )
        self.assertEqual(response.status_code, 406)

    def test_can_not_register_user_with_long_username(self):
        response = self.client.post(
                                    self.register_url,
                                    self.user_with_long_name,
                                    format='text/html'
                                    )
        self.assertEqual(response.status_code, 406)

    def test_can_not_register_user_with_non_alphanumeric_username(self):
        response = self.client.post(
                                    self.register_url,
                                    self.user_with_non_alphanumeric,
                                    format='text/html'
                                    )
        self.assertEqual(response.status_code, 400)

    def test_can_not_register_user_with_no_match_password(self):
        response = self.client.post(
                                    self.register_url,
                                    self.user_with_no_match_password,
                                    format='text/html'
                                    )
        self.assertEqual(response.status_code, 404)

    def test_can_not_register_user_with_invalid_email(self):
        response = self.client.post(
                                    self.register_url,
                                    self.user_with_invalid_email,
                                    format='text/html'
                                    )
        self.assertEqual(response.status_code, 400)

    def test_can_not_register_user_with_taken_email(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(
                                    self.register_url,
                                    self.user_with_taken_email,
                                    format='text/html'
                                    )
        self.assertEqual(response.status_code, 409)

    def test_can_not_register_user_with_taken_name(self):
        self.client.post(self.register_url, self.user, format='text/html')
        response = self.client.post(
                                    self.register_url,
                                    self.user_with_taken_name,
                                    format='text/html'
                                    )
        self.assertEqual(response.status_code, 409)


class LoginTest(BaseTest):
    def test_show_login_page(self):
        response = self.client.get(self.login_url)
        self.assertTemplateUsed(response, 'account/login.html')
        self.assertEqual(response.status_code, 200)

    def test_empty_inputs_no_signin(self):
        response = self.client.post(
                                    self.login_url,
                                    self.user_empty_login,
                                    format='text/html'
                                    )
        message = 'All fields are required'
        self.assertEquals(response.status_code, 401, msg=message)

    def test_signin_user(self):
        self.client.post(self.register_url, self.user, format='text/html')
        self.user_verified = {
                              'username': self.user['username'],
                              'password': self.user['password1'],
                              'is_email_verified': True
                             }
        
    def test_signin_email_not_verified_user(self):
        self.client.post(self.register_url, self.user, format='text/html')
        username = self.user['username']
        password = self.user['password1']
        user = get_user_model().objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()
        self.user_login = {
                            'username': username,
                            'password': password,
                            'is_email_verified': False
                          }
        response = self.client.post(
                                    self.login_url,
                                    self.user_login,
                                    format='text/html'
                                    )
        message = f'Email is not verified,please check your inbox.'
        self.assertEquals(response.status_code, 401, msg=message)

    def test_invalid_input_signin(self):
        self.user_bad_inputs = {
                                'username': 'user#',
                                'password': 'password',
                                'is_email_verified': False
                                }
        response = self.client.post(
                                    self.login_url,
                                    self.user_bad_inputs,
                                    format='text/html'
                                    )
        message = 'Invalid credentials.'
        self.assertEquals(response.status_code, 401, msg=message)
        self.assertTemplateUsed(response, 'account/login.html')

    # def test_log_out_user(self):
    #     response = self.client.get(self.logout_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'account/confirm.html')


class ProfileTest(BaseTest):
    def test_should_create_user_profile(self):
        user = get_user_model().objects.create_user(
                                        username='testme',
                                        email='noreply@gmail.com',
                                        password='password'
                                        )
        user.set_password('password')
        user.is_active = True
        user.save()
        self.assertEqual(str(user), user.username)
        pr = Profile.objects.get(user=user)
        pr.street_address1 = 'street1'
        pr.street_address2 = 'street2'
        self.assertEqual(
                         str(pr),
                         f"{user.username}"
                         )
        msg = pr.full_address()
        self.assertEqual(str(msg), f'{pr.street_address1} {pr.street_address2}')
        self.assertEqual(pr.image_tag(), 'No image found')

    # def test_user_open_profile(self):
    #     self.client.post(self.register_url, self.user, format='text/html')
    #     username = self.user['username']
    #     password = self.user['password1']
    #     self.user_login = {'username': username, 'password': password}
    #     self.client.post(self.login_url, self.user_login)
    #     response = self.client.get(self.profile_url)
    #     self.assertTemplateUsed(response, 'account/profile.html')
