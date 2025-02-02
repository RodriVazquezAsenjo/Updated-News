from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import all_news_articles, selected_news_article, add_article, add_organization, profile_modifications, profile_view, all_organizations, selected_organizations, like, bookmark, bookmark_list, news_edit, news_delete


class TestUrls(SimpleTestCase):

    def test_news_list_url_resolves(self):
        url = reverse('news_list')
        self.assertEqual(resolve(url).func, all_news_articles)

    def test_add_article_url_resolves(self):
        url = reverse('add_article')
        self.assertEqual(resolve(url).func, add_article)

    def test_profile_view_url_resolves(self):
        url = reverse('user_profile', kwargs={'username': 'testuser'})
        self.assertEqual(resolve(url).func, profile_view)

    def test_profile_modifications_url_resolves(self):
        url = reverse('profile_modifications', kwargs={'username': 'testuser'})
        self.assertEqual(resolve(url).func, profile_modifications)

    def test_news_edit_url_resolves(self):
        url = reverse('news_edit', kwargs={'slug': 'test-article'})
        self.assertEqual(resolve(url).func, news_edit)

    def test_news_delete_url_resolves(self):
        url = reverse('news_delete', kwargs={'slug': 'test-article'})
        self.assertEqual(resolve(url).func, news_delete)

    def test_organizations_list_url_resolves(self):
        url = reverse('organizations_list')
        self.assertEqual(resolve(url).func, all_organizations)

    def test_selected_organization_url_resolves(self):
        url = reverse('organization_detail', kwargs={'slug': 'test-org'})
        self.assertEqual(resolve(url).func, selected_organizations)

    def test_add_organization_url_resolves(self):
        url = reverse('add_organization')
        self.assertEqual(resolve(url).func, add_organization)

    def test_news_article_bookmark_url_resolves(self):
        url = reverse('news_article_bookmark', kwargs={'slug': 'test-article'})
        self.assertEqual(resolve(url).func, bookmark)

    def test_news_article_like_url_resolves(self):
        url = reverse('news_article_like', kwargs={'slug': 'test-article'})
        self.assertEqual(resolve(url).func, like)

    def test_bookmark_list_url_resolves(self):
        url = reverse('bookmark_list')
        self.assertEqual(resolve(url).func, bookmark_list)

    def test_news_detail_url_resolves(self):
        url = reverse('news_detail', kwargs={'slug': 'test-article'})
        self.assertEqual(resolve(url).func, selected_news_article)
