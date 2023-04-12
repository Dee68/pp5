from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.index, name='profile'),
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin')
]
