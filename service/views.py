import csv
import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage

from service.forms import PostFrom, CommentFrom, UserRegisterForm, MessageFrom
from service.models import Post, Comment


def index(request):
    return render(request, 'index.html')


# def test_fnc(user):
#     return True
#
#
# @user_passes_test(test_fnc)
def about(request):
    form = MessageFrom()
    if request.method == 'POST':
        form = MessageFrom(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            try:
                # send_mail(subject, body, EMAIL_HOST_USER, ['ricepob427@yasiok.com'], fail_silently=False)
                form.save()
            except Exception as err:
                print(err)
            return redirect('about')
    return render(request, 'about.html', {'form': form})


class RegisterForm(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь %(username)s был создан'


class PostsView(ListView):
    model = Post
    template_name = 'index.html'
    ordering = ['-created_at']


class DetailPostsView(DetailView):
    model = Post
    template_name = 'detail_post.html'


# class CreatePostsView(PermissionRequiredMixin, CreateView):
#     permission_required = 'service.add_post'
#     model = Post
#     template_name = 'create_post.html'
#     form_class = PostFrom
#     success_url = reverse_lazy('index')


@login_required
@permission_required('service.add_post')
def create_post(request):
    form = PostFrom()
    if request.method == 'POST':
        form = PostFrom(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            if title.lower() not in description.lower():
                messages.error(request, f'Описание поста {title}не содержит названия!')
                return redirect('index')
            messages.success(request, f'Пост {title} был успешно зоздан')
            return redirect('index')
    return render(request, 'create_post.html', {'form': form})


class UpdatePostsView(PermissionRequiredMixin, UpdateView):
    permission_required = 'service.change_post'
    model = Post
    template_name = 'create_post.html'
    form_class = PostFrom
    success_url = reverse_lazy('index')


class DeletePostsView(PermissionRequiredMixin, DeleteView):
    permission_required = 'service.delete_post'
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('index')


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'add_comment.html'
    form_class = CommentFrom

    # success_url = reverse_lazy('detail_post')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_post', kwargs={'pk': self.kwargs['pk']})


@staff_member_required
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        file_storage = FileSystemStorage()
        file_storage.save(uploaded_file.name, uploaded_file)
        name = file_storage.save(uploaded_file.name, uploaded_file)
        context = {'url': file_storage.url(name), 'name': uploaded_file.name}
    return render(request, 'upload.html', context)


def download(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(('Title', 'Description', 'Created_at'))

    for row in Post.objects.all().values_list('title', 'description', 'created_at'):
        writer.writerow(row)
    file_name = f'{datetime.datetime.now()} posts.csv'
    response['Content-Disposition'] = f'attachment; filename={file_name}'
    return response
