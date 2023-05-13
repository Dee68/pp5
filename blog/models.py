from django.db import models
from django.conf import settings


class Article(models.Model):
    STATUS = ((0, "Draft"), (1, "Published"))
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
                                settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE
                                )
    status = models.IntegerField(choices=STATUS, default=0)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    article_img = models.ImageField(blank=True, upload_to='blog/')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
                                    settings.AUTH_USER_MODEL,
                                    related_name='blogpost_likes',
                                    blank=True
                                    )

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    article = models.ForeignKey(
                                Article,
                                on_delete=models.CASCADE,
                                related_name='comments'
                                )
    email = models.EmailField()
    user = models.ForeignKey(
                             settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE
                             )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.user.username}'
