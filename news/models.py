from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from news.resources import *


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        articles = Post.objects.filter(author=self)
        article_rating = articles.aggregate(Sum('rating')).get('rating__sum') * 3
        comments = Comment.objects.filter(user=self.user)
        comment_rating = comments.aggregate(Sum('rating')).get('rating__sum')
        others_comments = Comment.objects.filter(post__author=self)
        others_comments_rating = others_comments.aggregate(Sum('rating')).get('rating__sum')
        overall = sum((article_rating, comment_rating, others_comments_rating))
        self.rating = overall
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    type = models.CharField(max_length=1, choices=TYPES, default=article)
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        prev_text = self.text[:125]
        return f'{prev_text}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
