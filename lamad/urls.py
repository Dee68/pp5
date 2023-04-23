"""lamad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


admin.site.index_title = 'Lamad Shop Administraion'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('shop/', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('whishlist/', include('wishlist.urls')),
    path('blog/', include('blog.urls')),
    path('contact/', include('contact.urls')),
    path('', include('home.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('summernote/', include('django_summernote.urls')),
    # ~~~~~~ password reset ~~~~~~~~~~~~~~~~~~~~~~
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_sent.html'
    ), name='password_reset_done'),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='account/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
        ),
    path(
        'password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='account/password_reset_complete.html'
        ),
        name='password_reset_complete'
        ),
    # ~~~~~~~~~~~~~ end password reset ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "lamad.views.page_not_found_view"  # custom 404 handler
handler500 = "lamad.views.internal_server_error"  # cuctom 500 handler
