from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Snippet


class ModelTestSuite(TestCase):
    """ Test suite for the Snippet model.
    """

    def setUp(self):
        self.user = User.objects.create(username="Test User", password="password")
        self.snippet = Snippet(
            title="Test Snippet",
            content="Test content",
            owner=self.user,
        )
        self.snippet.save()

    def test_can_create_snippet(self):
        old_count = Snippet.objects.count()
        new_snippet = Snippet(
            title="Test Snippet",
            content="Test content",
            owner=self.user,
        )
        new_snippet.save()
        new_count = Snippet.objects.count()

        self.assertNotEqual(new_count, old_count)

    def test_can_edit_snippet(self):
        snippet = Snippet.objects.all().first()
        snippet.title = "Updated Test Snippet"
        snippet.save()

        self.assertEqual(snippet.title, "Updated Test Snippet")


class ViewsTestSuite(TestCase):
    """ Test suite for the API views.
    """
    def setUp(self):
        self.client = APIClient()
        self.snippet_data = {
            'title': 'Sample snippet',
            'content': 'Here is some content to go with that',
            'is_private': False
            }
        self.private_snippet_data = {
            'title': 'Sample snippet',
            'content': 'Here is some content to go with that',
            'is_private': True
            }
        self.user = User.objects.create(username="TestUser", password="password")
        self.client.force_authenticate(user=self.user)

    def test_create_snippet(self):
        """ Test snippet creation via the API.
        """
        response = self.client.post(reverse('snippets-list'), self.snippet_data,
                                            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_own_snippet(self):
        response = self.client.post(reverse('snippets-list'), self.snippet_data,
                                    format='json')

        view_response = self.client.get(reverse('snippets-list'), kwargs={'pk': response.data['id']},
                                            format='json')

        self.assertEqual(view_response.status_code, 200)

    def test_view_private_snippet_without_ownership(self):
        response = self.client.post(reverse('snippets-list'), self.private_snippet_data,
                                    format='json') 

        client = APIClient()
        user = User.objects.create(username="RandomUser", password="password")
        client.force_authenticate(user=user)       

        view_response = client.get(reverse('snippets-list'), kwargs={'pk': response.data['id']},
                                            format='json')

        self.assertEqual(view_response.status_code, 403)

    def test_view_private_snippet_without_auth(self):
        response = self.client.post(reverse('snippets-list'), self.private_snippet_data,
                                    format='json')        
        client = APIClient()
        view_response = client.get(reverse('snippets-list'), kwargs={'pk': response.data['id']},
                                            format='json')

        self.assertEqual(view_response.status_code, 200)        

    def test_view_snippets_list(self):
        response = self.client.post(reverse('snippets-list'), self.private_snippet_data,
                                    format='json')        

        view_response = self.client.get(reverse('snippets-list'), format='json')

        self.assertEqual(view_response.status_code, status.HTTP_200_OK)

    def test_create_snippet_without_auth(self):
        client = APIClient()
        response = client.post(reverse('snippets-list'), self.snippet_data,
                               format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_own_snippet(self):
        response = self.client.post(reverse('snippets-list'), self.snippet_data,
                                    format='json')
        updated_response = self.client.patch(reverse('snippets-detail', kwargs={'pk': response.data['id']}),
                                           {'title': 'New title', 'is_private': True},
                                           format='json')

        self.assertEqual(updated_response.data['title'], 'New title')
        self.assertTrue(updated_response.data['is_private'])

    def test_edit_public_snippet_without_ownership(self):
        response = self.client.post(reverse('snippets-list'), self.snippet_data,
                                    format='json')        
        
        client = APIClient()
        user = User.objects.create(username="RandomUser", password="password")
        client.force_authenticate(user=user)

        edit_response = client.patch(reverse('snippets-detail', kwargs={'pk': response.data['id']}),
                                    {'title': 'New title', 'is_private': True},
                                    format='json')

        self.assertEqual(edit_response.status_code, 403)

    def test_edit_private_snippet_without_ownership(self):
        response = self.client.post(reverse('snippets-list'), self.private_snippet_data,
                                    format='json')        
        
        client = APIClient()
        user = User.objects.create(username="RandomUser", password="password")
        client.force_authenticate(user=user)

        edit_response = client.patch(reverse('snippets-detail', kwargs={'pk': response.data['id']}),
                                    {'title': 'New title', 'is_private': True},
                                    format='json')

        self.assertEqual(edit_response.status_code, 404)

    def test_view_public_snippet_without_ownership(self):
        response = self.client.post(reverse('snippets-list'), self.snippet_data,
                                    format='json')
        
        client = APIClient()
        user = User.objects.create(username="RandomUser", password="password")
        client.force_authenticate(user=user)

        view_response = client.get(reverse('snippets-detail', kwargs={'pk': response.data['id']}),
                                   format='json')

        self.assertEqual(view_response.status_code, 200)

    def test_view_private_snippet_without_ownership(self):
        response = self.client.post(reverse('snippets-list'), self.private_snippet_data,
                                    format='json')
        
        client = APIClient()
        user = User.objects.create(username="RandomUser", password="password")
        client.force_authenticate(user=user)

        view_response = client.get(reverse('snippets-detail', kwargs={'pk': response.data['id']}),
                                   format='json')

        self.assertEqual(view_response.status_code, 404)        

    def test_edit_public_snippet_without_auth(self):
        response = self.client.post(reverse('snippets-list'), self.snippet_data,
                                    format='json')
        client = APIClient()
        edit_response = client.patch(reverse('snippets-detail', kwargs={'pk': response.data['id']}),
                                    {'title': 'New title', 'is_private': True},
                                    format='json')
        self.assertEqual(edit_response.status_code, 401)

    def test_delete_public_snippet(self):
        response = self.client.post(reverse('snippets-list'), self.snippet_data,
                                    format='json')
        delete_response = self.client.delete(reverse('snippets-detail', kwargs={'pk': response.data['id']}),
                                             format='json')

        self.assertEqual(delete_response.status_code, 204)

    def test_delete_public_snippet_without_auth(self):
        response = self.client.post(reverse('snippets-list'), self.snippet_data,
                                    format='json')
        client = APIClient()
        delete_response = client.delete(reverse('snippets-list'), kwargs={'pk': response.data['id']},
                                        format='json')

        self.assertEqual(delete_response.status_code, 401)

