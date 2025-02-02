from django.test import TestCase
from django.contrib.auth.models import User
from .models import NewsArticles, UserProfile, Organizations, Comment

class ModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.organization = Organizations.objects.create(name='Test Org', slug='test-org', description='Test Description', country='GB')
        self.user_profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.article = NewsArticles.objects.create(title='Test Article', slug='test-article', content='Test content', author=self.user_profile)
        self.article.likes.set([self.user_profile])
        self.comment = Comment.objects.create(content='Test Comment', news_article=self.article, commenter=self.user_profile)
    
    def test_organization_str(self):
        self.assertEqual(str(self.organization), 'Test Org')
    
    def test_user_profile_str(self):
        self.assertEqual(str(self.user_profile), 'testuser')
    
    def test_news_article_str(self):
        self.assertEqual(str(self.article), 'Test Article')
    
    def test_comment_str(self):
        self.assertEqual(str(self.comment), 'Comment Test Comment by testuser')
    
    def test_total_likes(self):
        self.assertEqual(self.article.total_likes(), 1)
    
    def test_total_comments(self):
        self.assertEqual(self.article.total_comments(), 1)
    
