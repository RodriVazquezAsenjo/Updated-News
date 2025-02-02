from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import NewsArticles, UserProfile, Organizations

class NewsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='testuser', password='password')
        self.user_profile, created = UserProfile.objects.update_or_create(user=self.user,)
        self.article = NewsArticles.objects.create(title='Test Article', slug='test-article', content='Test content', author=self.user_profile)
        self.organization = Organizations.objects.create(name='Test Org', slug='test-org', description='Test Description', country='GB')


    def test_all_news_articles_view(self):
        response = self.client.get(reverse('news_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_list.html')

    def test_selected_news_article_view(self):
        response = self.client.get(reverse('news_detail', kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_detail.html')

    def test_add_article_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('add_article'), {'title': 'New Article', 'content': 'Some content'})
        self.assertEqual(response.status_code, 302)  # Should redirect after successful form submission

    def test_like_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('news_article_like', kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 302)  # Should redirect after liking

    def test_bookmark_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('news_article_bookmark', kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 302)  # Should redirect after bookmarking

    def test_profile_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('user_profile', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/profile.html')

    def test_profile_modifications_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('profile_modifications', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/profile_modifications.html')

    def test_all_organizations_view(self):
        response = self.client.get(reverse('organizations_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/organization_list.html')

    def test_selected_organization_view(self):
        response = self.client.get(reverse('organization_detail', kwargs={'slug': self.organization.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/organization_detail.html')