from django.urls import path
from .views import ArticleList, ArticleDetail, ArticleLike

app_name = 'blog'


urlpatterns = [
    path('', ArticleList.as_view(), name='articles'),
    path('<slug:slug>/', ArticleDetail.as_view(), name='article_detail'),
    path('like/<slug:slug>/', ArticleLike.as_view(), name='article_like'),
]
