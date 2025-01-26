from .models import Comment, UserProfile, News, Organization
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'affiliation'
        ]

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'description', 'founded', 'country']