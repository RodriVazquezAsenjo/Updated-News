from django.test import TestCase
from .forms import CommentForm, UserProfileForm, AddArticleForm, OrganizationsForm
from .models import Comment, UserProfile, NewsArticles, Organizations


class CommentFormTest(TestCase):
    def test_valid_comment_form(self):
        form = CommentForm(data={'content': 'This is a test comment'})
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        form = CommentForm(data={'content': ''})
        self.assertFalse(form.is_valid())


class UserProfileFormTest(TestCase):
    def test_valid_user_profile_form(self):
        form = UserProfileForm(
            data={
                'affiliated': None,
                'nationality': 'US',
                'bio': 'Test bio'
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_user_profile_form(self):
        form = UserProfileForm(
            data={
                'affiliated': '',
                'nationality': '',
                'bio': ''
                }
            )
        self.assertFalse(form.is_valid())


class AddArticleFormTest(TestCase):
    def test_valid_article_form(self):
        form = AddArticleForm(
            data={
                'title': 'Test Article',
                'content': 'This is test content',
                'image': None
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_article_form(self):
        form = AddArticleForm(data={'title': '', 'content': '', 'image': None})
        self.assertFalse(form.is_valid())


class OrganizationsFormTest(TestCase):
    def test_valid_organization_form(self):
        form = OrganizationsForm(
            data={
                'name': 'Test Org',
                'description': 'Test Description',
                'foundation': '2025-01-01',
                'country': 'US',
                'image': None
                }
            )
        self.assertTrue(form.is_valid())

    def test_invalid_organization_form(self):
        form = OrganizationsForm(
            data={
                'name': '',
                'description': '',
                'foundation': '',
                'country': '',
                'image': None
                }
            )
        self.assertFalse(form.is_valid())
