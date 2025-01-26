from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
        'page_title': organization.name,
        'organization': organization
    }

    return render(request, template, context)