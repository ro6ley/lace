from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Template


class ModelTestSuite(TestCase):
    """ Test suite for the Template model.
    """

    def setUp(self):
        self.user = User.objects.create(username="Test User", password="password")
        self.template = Template(
            title="Test Template",
            content="Test content",
            owner=self.user,
        )
        self.template.save()

    def test_can_create_template(self):
        old_count = Template.objects.count()
        new_template = Template(
            title="Test Template",
            content="Test content",
            owner=self.user,
        )
        new_template.save()
        new_count = Template.objects.count()

        self.assertNotEqual(new_count, old_count)


    def test_can_edit_template(self):
        template = Template.objects.all().first()
        template.title = "Updated Test Template"
        template.save()

        self.assertEqual(template.title, "Updated Test Template")

    def test_can_delete_template(self):
        pass


class ViewsTestSuite(TestCase):
    """ Test suite for the API views.
    """
    def setUp(self):
        self.client = APIClient()
        self.template_data = {
            'title': 'Sample template',
            'content': 'Here is some content to go with that',
            'is_private': False
            }
        self.user = User.objects.create(username="Test User", password="password")
        self.client.force_authenticate(user=self.user)

    def test_create_template(self):
        """ Test template creation via the API.
        """
        response = self.client.post(reverse('templates'), self.template_data,
                                            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_template_without_auth(self):
        client = APIClient()
        response = client.post(reverse('templates'), self.template_data,
                               format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_template(self):
        pass

    def test_edit_template_without_ownership(self):
        pass

    def test_edit_template_without_auth(self):
        pass

    def test_delete_template(self):
        pass

    def test_delete_template_without_auth(self):
        pass


class UserManagementTestSuite(TestCase):
    """ Test suite for user management
    """

    def setUp(self):
        self.client = APIClient()

    def test_user_sign_up_sign_in(self):
        user_data = {
            'username': 'test_username',
            'email': 'test@email.com',
            'password': 'ojuelegba1',
            'password1': 'ojuelegba1',
            'password2': 'ojuelegba1'
        }
        sign_up_response = self.client.post('/auth/register/', user_data)

        self.assertEqual(sign_up_response.status_code, status.HTTP_201_CREATED)

        sign_in_response = self.client.post('/auth/login/', user_data)

        self.assertEqual(sign_in_response.status_code, status.HTTP_200_OK)
