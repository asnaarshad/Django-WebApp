from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve
from django.db.models import Q

import hashlib

# Unused Import
import sys  # Positive Case – unused
import os  # Negative Case – used
print(os.name)


# Rule 1: SQL Injection
# Tool: SQLMap
# Positive Case (Vulnerable) 
from django.http import HttpResponse
from django.db import connection

def vulnerable_sql(request):
    user_id = request.GET.get('id')
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM auth_user WHERE id = {user_id};")
        result = cursor.fetchone()
    return HttpResponse(f"User: {result}")

# Negative Case (Secure)
def secure_sql(request):
    user_id = request.GET.get('id')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM auth_user WHERE id = %s;", [user_id])
        result = cursor.fetchone()
    return HttpResponse(f"User: {result}")

# Rule 2: XSS (Cross-Site Scripting)
# Tool: OWASP ZAP
# Positive Case
def xss_vulnerable(request):
    name = request.GET.get("name", "")
    return HttpResponse(f"Hello {name}")

# Negative Case (Secure)
from django.utils.html import escape

def xss_secure(request):
    name = escape(request.GET.get("name", ""))
    return HttpResponse(f"Hello {name}")


# Flake8 Rules 
# Line Too Long
print("This is a very long line that exceeds the PEP8 79 character limit, so flake8 should complain about it.")  # Positive Case



# bandit rule: md5()
def weak_hash(password):
    return hashlib.md5(password.encode()).hexdigest()  # Positive Case

def strong_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()  # Negative Case


# bandit rule: eval()
def insecure_eval(user_input):
    return eval(user_input)  # Positive Case – Bandit will flag this

def secure_cast(user_input):
    return int(user_input) * 2  # Negative Case – Safe alternative


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def search(request):
    template='blog/home.html'

    query=request.GET.get('q')

    result=Post.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    paginate_by=2
    context={ 'posts':result }
    return render(request,template,context)
   


def getfile(request):
   return serve(request, 'File')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
