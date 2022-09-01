from django.db import models
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(verbose_name='название', max_length=100)
    description = models.TextField(verbose_name='описание', blank=True)
    image = models.ImageField(verbose_name='картинка', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата изменения', auto_now=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('index')


class Comment(models.Model):
    description = models.TextField(verbose_name='описание', blank=True)
    created_at = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Message(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=100, null=True, blank=True)
    body = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.body
