from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from .views import (index,
                    logout_page,
                    confirm_page,
                    RegistrationView,
                    LoginView,
                    validate_email,
                    validate_username,
                    VerificationView
                    )

app_name = 'account'

urlpatterns = [
    path('', index, name='profile'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('signin/', LoginView.as_view(), name='signin'),
    path(
        'validate-username',
        csrf_exempt(validate_username), name='validate-username'),
    path(
        'validate-email',
        csrf_exempt(validate_email), name='validate-email'),
    path('activate/<uidb64>/<token>/',
         VerificationView.as_view(),
         name='activate'
         ),
    path('confirmation', confirm_page, name='confirmation'),
]
