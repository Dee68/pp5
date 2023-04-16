from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.whish_list, name='wish_list'),
    path('add_to_wishlist/', views.add_to_wish_list, name='add_to_wishlist'),
    path('delete_item/', views.delete_item, name='delete_item')
]
