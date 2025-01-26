from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from .models import News, UserProfile, Comment, Likes, Organization
from .forms import CommentForm, NewsForm, OrganizationForm, UserProfileForm


def all_news(request):
    news = News.objects.all()
    template = 'news/news_list.html'
    context = {
        'page_title': 'Feed',
        'news': news
    }
    return render(request, template, context)

@login_required
def detail_news(request, slug):
    news_article = get_object_or_404(News, slug=slug)
    new_comment = None

    like_count = news_article.likes.count()
    comment_count = news_article.comments.count()

    if request.method == 'POST':
        if 'like' in request.POST:
            like = Likes.objects.filter(news_article=news_article, user=request.user).first()
            if like:
                like.delete()
                like_count -= 1
            else:
                Likes.objects.create(user=request.user, news_article=news_article)
                like_count += 1

        if 'read_later' in request.POST:
            if request.user in news_article.read_later.all():
                news_article.read_later.remove(request.user)
            else:
                news_article.read_later.add(request.user)

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news_article
            new_comment.commenter = request.user
            new_comment.save()

        return redirect(news_article.get_absolute_url())

    else:
        comment_form = CommentForm()

    template = 'news/news_detail.html'
    context = {
        'page_title': news_article.title,
        'news_article': news_article,
        'comment_form': comment_form,
        'liked': Likes.objects.filter(news_article=news_article, user=request.user).exists(),
        'read_later': request.user in news_article.read_later.all(),
        'like_count': like_count,
        'comment_count': comment_count,
    }

    return render(request, template, context)

@login_required
def add_article(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news_article = form.save(commit=False)
            news_article.author = request.user
            news_article.slug = slugify(news_article.title)
            if request.user.profile.active and request.user.profile.affiliation:
                news_article.affiliation = request.user.profile.affiliation
            news_article.save()
            return redirect('news_list')
    else:
        form = NewsForm()

    template = 'news/add_article.html'
    context = {
        'form': form
    }
    return render(request, template, context)

class ReadLater(LoginRequiredMixin, generic.ListView):
    model = News
    template_name = 'news/read_later.html'
    context_object_name = 'read_later'
    paginate_by = 6

    def get_queryset(self):
        return self.request.user.read_later_news.all()


class UserProfileDetailView(generic.DetailView):
    model = UserProfile
    template_name = 'news/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return get_object_or_404(UserProfile, user=user)

@login_required
def profile_modifications (request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)

    if request.user.username != username:
        return redirect('profile_detail', username=request.user.username)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.affiliation = request.user.profile.affiliation
            profile.save()
            return redirect('profile_detail', username=request.user.username)
    else:
        profile_form = UserProfileForm(instance=user_profile)
    
    template = 'news/profile_modifications.html'
    context = {
        'profile_form': profile_form,
        'user_profile': user_profile
    }
    return render(request, template, context)

def OrganizationListView(request):
    organizations = Organization.objects.all()

    template = 'news/organization_list.html'
    context = {
        'page_title': 'Organizations',
        'organizations': organizations
    }

    return render(request, template, context)

def OrganizationDetailView(request, slug):
    organizations = get_object_or_404(Organization, slug=slug)

    template = 'news/organization_detail.html'
    context = {
        'page_title': organizations.name,
        'organization': organizations
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
            return redirect('organizations_list')
    else:
        form = OrganizationForm()

    template = 'news/add_organization.html'
    context = {
        'form': form
    }
    return render(request, template, context)