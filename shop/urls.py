from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.products, name='products'),
    path('<slug:category_slug>', views.products, name='products_by_category'),
    path('<int:product_id>/',
         views.product_detail, name='product_detail'),
#     path('add_review/<int:product_id>/', views.add_review, name='add_review'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/',
         views.delete_product, name='delete_product'),
]
