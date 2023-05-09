from django.shortcuts import (
    render,
    get_object_or_404,
    HttpResponseRedirect,
    reverse
    )
from django.views import generic, View
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from .models import Article, Comment
from .forms import CommentForm


class ArticleList(generic.ListView):
    model = Article
    template_name = 'blog/blog.html'
    queryset = Article.objects.filter(status=1).order_by('-created_on')
    paginate_by = 6


class ArticleDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Article.objects.filter(status=1)
        article = get_object_or_404(queryset, slug=slug)
        comments = article.comments.order_by('created_on')
        comment_form = CommentForm()
        liked = False
        if article.likes.filter(id=self.request.user.id).exists():
            liked = True
        template_name = 'blog/article_detail.html'
        context = {
            'article': article,
            'comments': comments,
            'liked': liked,
            'comment_form': comment_form
        }
        return render(request, template_name, context)

    def post(self, request, slug, *args, **kwargs):
        queryset = Article.objects.filter(status=1)
        article = get_object_or_404(queryset, slug=slug)
        comments = article.comments.order_by("-created_on")
        user = request.user
        liked = False
        if article.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment_form.instance.user.email = request.user.email
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.save()
            messages.success(request,
                             'Your comment has been posted')
        else:
            comment_form = CommentForm()
            messages.warning(request,
                             'Something went wrong. Please Try Again')

        template = "blog/article_detail.html"
        context = {
            'article': article,
            'comments': comments,
            'liked': liked,
            'user': user,
            'comment_form': comment_form

        }
        return render(request, template, context)


class ArticleLike(View):
    """Method to like a post"""
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug)

        if article.likes.filter(id=request.user.id).exists():
            article.likes.remove(request.user)
        else:
            article.likes.add(request.user)

        return HttpResponseRedirect(
                                    reverse(
                                            'blog:article_detail',
                                            args=[slug]
                                             )
                                    )
