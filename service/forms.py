from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from service.models import Post, Comment, Message


class PostFrom(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'description': forms.Textarea(attrs={'class': 'form-control'})}


class CommentFrom(ModelForm):
    class Meta:
        model = Comment
        fields = ['description']
        widgets = {'description': forms.Textarea(attrs={'class': 'form-control'})}


class MessageFrom(ModelForm):
    class Meta:
        model = Message
        fields = ['title', 'body']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'body': forms.Textarea(attrs={'class': 'form-control'})}


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
