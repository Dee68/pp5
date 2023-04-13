from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from django_countries.fields import CountryField
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']


class ImageForm(ModelForm):
    """Image form to update profile picture"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Profile
        fields = ['avatar']


class AddressForm(ModelForm):
    """Address form to change shipping information"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Submit'))
        self.fields['street_address2'].required = False
        self.fields['county'].required = False
        self.fields['postcode'].required = False

    street_address1 = forms.CharField(max_length=100)
    street_address2 = forms.CharField(max_length=100)
    town_or_city = forms.CharField(max_length=30)
    county = forms.CharField(max_length=30)
    postcode = forms.CharField(max_length=30)
    country = CountryField(max_length=5)

    class Meta:
        model = Profile
        fields = ['street_address1', 'street_address2', 'town_or_city',
                  'county', 'postcode', 'country']
