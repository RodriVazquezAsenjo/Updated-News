from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
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
    #comment logic
    new_comment = None
    comment_form = CommentForm()
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news_article = selected_news_article
            new_comment.commenter = request.user
            new_comment.save()
            return redirect('news_detail', slug=selected_news_article.slug)
    context = {
        'selected_news_article': selected_news_article,
        'new_comment': new_comment, 
        'comment_form': comment_form
    }
    return render(request, template, context)

@login_required
def like(request, slug):
	#likes logic
    #obtain the object from NewsArticles where the slug is equal to the slug of the object. 
	selected_news_article = get_object_or_404(NewsArticles, slug=slug)
    #we filter the object and say that if the selected article's like list has the id from the user_profile
	if selected_news_article.likes.filter(id=request.user.user_profile.id):
        #then we remove the user_profile from the list
		selected_news_article.likes.remove(request.user.user_profile)
	else:
        #otherwise, add the user_profile. 
		selected_news_article.likes.add(request.user.user_profile)
        #after this is done return it to the news_list page. 
	return redirect('news_list')
	
@login_required
def bookmark(request, slug):
    selected_news_article = get_object_or_404(NewsArticles, slug=slug)
    if selected_news_article.bookmark.filter(id=request.user.user_profile.id):
        selected_news_article.bookmark.remove(request.user.user_profile)
    else:
        selected_news_article.bookmark.add(request.user.user_profile)

    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)
    
	
@login_required
def add_article(request):
    if request.method == 'POST':
        form = AddArticleForm(request.POST)
        if form.is_valid():
            news_article = form.save(commit=False)
            news_article.author = request.user.user_profile
            news_article.slug = slugify(news_article.title)
            if request.user.user_profile.affiliated:
                news_article.organization = request.user.user_profile.affiliated
            news_article.save()
            return redirect('news_list')
    else:
        form = AddArticleForm()

    template = 'add_article.html'
    context = {
        'form': form
    }
    return render(request, template, context)

@login_required
def profile_view(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)
    template = 'news/profile.html'
    context = {
        'user_profile': user_profile
    }
    return (request, template, context)

@login_required
def profile_modifications(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)

    if request.user.user_profile.pk != pk:
        return redirect('profile_detail', pk=request.user.user_profile.pk)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.affiliated = request.user.user_profile.affiliated
            profile.save()
            return redirect('profile_detail', pk=request.user.user_profile.pk)
    else:
        profile_form = UserProfileForm(instance=user_profile)

    template = 'news/profile_modifications.html'
    context = {
        'profile_form': profile_form,
        'user_profile': user_profile
    }
    return render(request, template, context)
    
def BookMark(request):
	bookmarked_news_articles = NewsArticles.objects.filter(author__affiliated=organization)
	template = 'news/bookmark.html'
	context = {
		'title': FEED,
		'bookmarked_news_articles': bookmarked_news_articles,
		}
	return(request, template, context)
    
def all_organizations(request):
    organizations = Organizations.objects.all()

    template = 'news/organization_list.html'
    context = {
        'page_title': 'Organizations',
        'organizations': organizations
    }

    return render(request, template, context)

def selected_organizations(request, slug):
    organization = get_object_or_404(Organizations, slug=slug)

    template = 'news/organization_detail.html'
    context = {
        'page_title': organization.name,
        'organization': organization
    }

    return render(request, template, context)

@login_required
def add_organization(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.slug = slugify(organization.name) 
            organization.save()
            return redirect('organization_list')
    else:
        form = OrganizationForm()

    template = 'news/add_organization.html'
    context = {
        'form': form
    }
    return render(request, template, context)