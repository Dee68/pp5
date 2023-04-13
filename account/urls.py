from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from .views import (index,
                    signin,
                    RegistrationView,
                    validate_email,
                    validate_username
                    )

app_name = 'account'

urlpatterns = [
    path('', index, name='profile'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('signin/', signin, name='signin'),
    path(
        'validate-username',
        csrf_exempt(validate_username), name='validate-username'),
    path(
        'validate-email',
        csrf_exempt(validate_email), name='validate-email'),
    # path('confirmation', views.confirm_page, name='confirmation'),
]
