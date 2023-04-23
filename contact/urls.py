from django.urls import path
from . import views

app_name = 'contact'


urlpatterns = [
    path('', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('shipping/', views.shipping, name='shipping'),
    path('returns/', views.returns, name='returns'),
    path('about/', views.about, name='about'),
]
