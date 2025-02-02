from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.contrib import messages
from .models import NewsArticles, UserProfile, Comment, Organizations
from .forms import CommentForm, AddArticleForm, OrganizationsForm, UserProfileForm
from urllib.parse import urlparse


def all_news_articles(request):
    all_news_articles = NewsArticles.objects.all()
    template = 'news/news_list.html'
    context = {
        'title': 'FEED',
        'all_news': all_news_articles,
    }
    return render(request, template, context)


def selected_news_article(request, slug):
    selected_news_article = get_object_or_404(NewsArticles, slug=slug)
    template = 'news/news_detail.html'
    # Comment logic
    new_comment = None
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news_article = selected_news_article
            new_comment.commenter = request.user.user_profile
            new_comment.save()
            messages.success(request, 'Your comment was added successfully!')
            return redirect('news_detail', slug=selected_news_article.slug)
    context = {
        'selected_news_article': selected_news_article,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    return render(request, template, context)


@login_required
def like(request, slug):
    selected_news_article = get_object_or_404(NewsArticles, slug=slug)
    if selected_news_article.likes.filter(id=request.user.user_profile.id):
        selected_news_article.likes.remove(request.user.user_profile)
        messages.success(request, 'You unliked the article.')
    else:
        selected_news_article.likes.add(request.user.user_profile)
        messages.success(request, 'You liked the article.')

    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)


@login_required
def bookmark(request, slug):
    selected_news_article = get_object_or_404(NewsArticles, slug=slug)
    if selected_news_article.bookmark.filter(id=request.user.user_profile.id):
        selected_news_article.bookmark.remove(request.user.user_profile)
        messages.success(request, 'You removed the article from your bookmark')
    else:
        selected_news_article.bookmark.add(request.user.user_profile)
        messages.success(request, 'You added the article to your bookmarks.')

    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)


@login_required
def add_article(request):
    if request.method == 'POST':
        form = AddArticleForm(request.POST, request.FILES)
        if form.is_valid():
            news_article = form.save(commit=False)
            news_article.author = request.user.user_profile
            news_article.slug = slugify(news_article.title)
            if request.user.user_profile.affiliated:
                news_article.organization = request.user.user_profile.affiliated
            news_article.save()
            messages.success(request, 'Article added successfully!')
            return redirect('news_list')
    else:
        form = AddArticleForm()

    template = 'news/add_article.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def profile_view(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    all_news_articles = NewsArticles.objects.filter(
        author=request.user.user_profile
        )
    template = 'news/profile.html'
    context = {
        'user_profile': user_profile,
        'all_news_articles': all_news_articles,
    }
    return render(request, template, context)


@login_required
def profile_modifications(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)

    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile', username=request.user.username)
    else:
        profile_form = UserProfileForm(instance=user_profile)

    template = 'news/profile_modifications.html'
    context = {
        'profile_form': profile_form,
        'user_profile': user_profile,
    }
    return render(request, template, context)


def bookmark_list(request):
    bookmarked_news_articles = NewsArticles.objects.filter(
        bookmark=request.user.user_profile
        )
    template = 'news/bookmark.html'
    context = {
        'title': 'BOOKMARK',
        'bookmarked_news_articles': bookmarked_news_articles,
    }
    return render(request, template, context)


def all_organizations(request):
    query = request.GET.get('q', '')
    if query:
        organizations = Organizations.objects.filter(name__icontains=query)
    else:
        organizations = Organizations.objects.all()
    template = 'news/organization_list.html'
    context = {
        'page_title': 'Organizations',
        'organizations': organizations,
    }

    return render(request, template, context)


def selected_organizations(request, slug):
    organization = get_object_or_404(Organizations, slug=slug)
    news_articles_from_organization = NewsArticles.objects.filter(
        author__affiliated=organization
        )
    template = 'news/organization_detail.html'
    context = {
        'page_title': organization.name,
        'organization': organization,
        'news_articles_from_organization': news_articles_from_organization,
    }

    return render(request, template, context)


@login_required
def add_organization(request):
    if request.method == 'POST':
        form = OrganizationsForm(request.POST, request.FILES)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.slug = slugify(organization.name)
            organization.save()
            messages.success(request, 'Organization added successfully!')
            return redirect('organizations_list')
    else:
        form = OrganizationsForm()

    template = 'news/add_organization.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def news_edit(request, slug):
    # Get the article by slug
    news_article = get_object_or_404(NewsArticles, slug=slug)

    # Check if the current user is the author of the article
    if news_article.author != request.user.user_profile:
        return redirect('news_detail', slug=slug)  # Redirect if not the author

    if request.method == 'POST':
        form = AddArticleForm(request.POST, instance=news_article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('news_detail', slug=news_article.slug)
    else:
        form = AddArticleForm(instance=news_article)

    template = 'news/edit_article.html'
    context = {
        'form': form,
        'news_article': news_article,
    }
    return render(request, template, context)


@login_required
def news_delete(request, slug):
    # Get the article by slug
    news_article = get_object_or_404(NewsArticles, slug=slug)

    # Check if the current user is the author of the article
    if news_article.author != request.user.user_profile:
        return redirect('news_detail', slug=slug)  # Redirect if not the author

    if request.method == 'POST':
        news_article.delete()
        messages.success(request, 'Article deleted successfully!')
        return redirect('news_list')  # Redirect to the news list

    template = 'news/delete_article.html'
    context = {
        'news_article': news_article,
    }
    return render(request, template, context)
