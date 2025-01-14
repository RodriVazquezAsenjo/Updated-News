from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.models import User
from .models import News, UserProfile
from .forms import CommentForm

class NewsList(generic.ListView):
    queryset = News.objects.all()
    template_name = "news/news_list.html"
    paginate_by = 12

class NewsDetail(generic.DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def post(self, request, *args, **kwargs):
        news = self.get_object()
        if 'like' in request.POST:
            news.likes += 1
            news.save()
        elif 'read_later' in request.POST:
            news.read_later_by.add(request.user)
        elif 'comment' in request.POST:
            content = request.POST.get('comment', '')
            if content:
                news.comments.create(author=request.user, content=content)
        return redirect(news)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class ReadLater(generic.ListView):
    model = News
    template_name = 'news/read_later.html'
    context_object_name = 'read_later'
    paginate_by = 12

class UserProfileDetailView(generic.DetailView):
    model = UserProfile
    template_name = 'news/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        # Fetch the UserProfile linked to the user with the specified pk (user.id)
        return get_object_or_404(UserProfile, user_id=self.kwargs['pk'])