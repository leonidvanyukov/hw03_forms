from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import Group, Post, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }

    return render(request, 'posts/index.html', context)

#    posts = Post.objects.all()[:settings.AMOUNT]
#    context = {
#        'posts': posts,
#    }
#    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
    }

#    posts = group.posts.all()[:settings.AMOUNT]
#    context = {
#        'group': group,
#        'posts': posts,
#    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    author_posts = author.posts.all()
    paginator = Paginator(author_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    posts_count = paginator.count
    context = {
        'username': author,
        'page_obj': page_obj,
        'posts_count': posts_count
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    posts = get_object_or_404(User, username=post.author)
    posts_count = posts.posts.count()
    context = {
        'post': post,
        'posts_count': posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if not request.method == 'POST':
        form = PostForm()
        return render(
            request,
            'posts/new_post.html',
            {'form': form, 'is_edit': False},
        )

    form = PostForm(request.POST,)
    if not form.is_valid():
        return render(
            request,
            'posts/new_post.html',
            {'form': form, 'is_edit': False}
        )

    post = form.save(commit=False)
    post.author = request.user
    post.pub_date = datetime.now()
    post.save()

    redirect_url = '/profile/' + request.user.username + '/'

    return redirect(redirect_url)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not post.author == request.user:
        redirect_url = '/profile/' + request.user.username + '/'
        return redirect(redirect_url)
    form = PostForm(
        request.POST or None,
        instance=post,
    )
    if not request.method == 'POST':
        return render(
            request,
            'posts/new_post.html',
            {'post': post, 'form': form, 'is_edit': True},
        )
    if not form.is_valid():
        return render(
            request,
            'posts/new_post.html',
            {'post': post, 'form': form, 'is_edit': True},
        )
    form.save()
    redirect_url = '/posts/' + str(post_id)
    return redirect(redirect_url)
