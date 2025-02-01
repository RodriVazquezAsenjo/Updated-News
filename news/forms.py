from .models import Comment, UserProfile, NewsArticles, Organizations
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['affiliated', 'nationality', 'bio']

class AddArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticles
        fields = ['title', 'content']

class OrganizationsForm(forms.ModelForm):
    class Meta:
        model = Organizations
        fields = ['name', 'description', 'foundation', 'country']