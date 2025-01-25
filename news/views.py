from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib.auth.models import User
from .models import News, UserProfile, Comment, Likes, Organization
from .forms import CommentForm


def all_news(request):
    news = News.objects.all()

    template = 'news/news_list.html'
    context = {
        'page_title': 'Feed',
        'news': news
    }


    return render(request, template, context)


def detail_news(request, slug):
    news_article = get_object_or_404(News, slug=slug)
    new_comment = None

    if request.method == 'POST':
        if 'like' in request.POST:
            existing_like = news_article.likes.filter(user=request.user).first()
            if existing_like:
                existing_like.delete()
            else:
                Like.objects.create(user=request.user, news=news_article)

        if 'read_later' in request.POST:
            if request.user in news_article.read_later.all():
                news_article.read_later.remove(request.user)
            else:
                news_article.read_later.add(request.user)

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news_article
            new_comment.author = request.user
            new_comment.save()

        return redirect(news_article.get_absolute_url())

    else:
        comment_form = CommentForm()

    template = 'news/news_detail.html'
    context = {
        'page_title': news_article.title,
        'news_article': news_article,
        'comment_form': comment_form,
        'liked': news_article.likes.filter(user=request.user).exists(),
        'read_later': request.user in news_article.read_later.all(),
    }

    return render(request, template, context)


class ReadLater(generic.ListView):
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
        return get_object_or_404(UserProfile, user_id=self.kwargs['pk'])


def OrganizationListView(request):
    organizations = Organization.objects.all()

    template = 'news/organization_list.html'
    context = {
        'page_title': 'Organizations',
        'organizations': organizations
    }

    return render(request, template, context)


def OrganizationDetailView(request, slug):
    organization = get_object_or_404(Organization, slug=slug)

    template = 'news/organization_detail.html'
    context = {
        'page_title': organization.name,
        'organization': organization
    }

    return render(request, template, context)