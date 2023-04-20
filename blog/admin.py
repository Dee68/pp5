from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Article, Comment


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'status', 'slug', 'created_on')
    list_filter = ('status', 'created_on')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'article', 'created_on')
    list_filter = ('created_on', 'user')
    search_fields = ('user', 'email', 'body')
