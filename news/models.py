from django.db import models


class User(models.Model):
    _first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    login = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class News(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ManyToManyField('Category', through='NewsCategories')


class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    category = models.ManyToManyField('Category', through='ArticlesCategories')


class Comment(models.Model):
    text = models.TextField()

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=255, null=True)


class ArticlesCategories(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class NewsCategories(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
