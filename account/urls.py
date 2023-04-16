from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from .views import (index,
                    logout_page,
                    order_history,
                    edit_image,
                    shipping_details,
                    edit_shipping,
                    order_history_details,
                    whishlist,
                    add_to_whishlist,
                    RegistrationView,
                    LoginView,
                    edit_profile,
                    validate_email,
                    validate_username,
                    VerificationView
                    )

app_name = 'account'

urlpatterns = [
    path('', index, name='profile'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('edit_profile/<user_id>', edit_profile, name='edit_profile'),
    path('edit_image/<user_id>', edit_image, name='edit_image'),
    path('order_history/', order_history, name='order_history'),
    path('shipping_details/', shipping_details, name='shipping_details'),
    path('edit_shipping/<user_id>', edit_shipping, name='edit_shipping'),
    path('order_history_details/<order_number>', order_history_details,
         name='order_history_details'),
    path('wishlist/', whishlist, name='whishlist'),
    path('add_to_whishlist/<prod_slug>', add_to_whishlist, name='add_to_whishlist'),
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
    path('logout/', logout_page, name='logout'),
]
