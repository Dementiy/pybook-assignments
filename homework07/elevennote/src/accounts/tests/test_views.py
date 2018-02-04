from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from accounts.views import RegisterView
from accounts.forms import UserCreationForm


User = get_user_model()

class RegisterViewTests(TestCase):

    def setUp(self):
        url = reverse('accounts:register')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/register/')
        self.assertEquals(view.func.view_class, RegisterView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):

    def setUp(self):
        url = reverse('accounts:register')
        data = {
            'email': 'user@example.com',
            'password1': 'secret',
            'password2': 'secret',
        }
        self.response = self.client.post(url, data)
        self.notes_page = reverse('notes:index')
        self.index_page = reverse('index')

    def test_redirects_to_index_page(self):
        self.assertRedirects(self.response, self.index_page,
            target_status_code=302)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.notes_page)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSingUpTests(TestCase):

    def setUp(self):
        url = reverse('accounts:register')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())

