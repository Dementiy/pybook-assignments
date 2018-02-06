from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

import datetime

from notes.models import Note
from notes.views import NoteList, NoteDetail

User = get_user_model()


class IndexTests(TestCase):

    def setUp(self):
        self.test_user1 = User.objects.create_user(
            email="test_user1@example.com",
            password="secret")
        self.test_user2 = User.objects.create_user(
            email="test_user2@example.com",
            password="secret")

        now = datetime.datetime.now()
        self.notes = []
        self.n = 10
        self.paginate_by = 5
        for i in range(self.n):
            self.notes.append(Note.objects.create(
                title=f"Note title {i}",
                body="Note description",
                pub_date=now + datetime.timedelta(days=i),
                owner=self.test_user1))

    def test_redirect_if_not_logged_in(self):
        index_page_url = reverse('notes:index')
        response = self.client.get(index_page_url)
        self.assertRedirects(response, "/accounts/login/?next=/notes/")

    def test_index_view_status_code(self):
        self.client.login(email="test_user1@example.com", password="secret")
        index_page_url = reverse('notes:index')
        response = self.client.get(index_page_url)
        self.assertEquals(response.status_code, 200)

    def test_index_url_resolves_index_view(self):
        view = resolve('/notes/')
        self.assertEquals(view.func.view_class, NoteList)

    def test_index_view_contains_link_to_details_page(self):
        self.client.login(email="test_user1@example.com", password="secret")
        index_page_url = reverse('notes:index')
        response = self.client.get(index_page_url)
        for note in response.context["latest_note_list"]:
            note_detail_url = reverse('notes:detail',
                kwargs={'pk': note.pk})
            self.assertContains(response, f'href="{note_detail_url}"')

    def test_notes_ordered_by_pub_dates(self):
        self.client.login(email="test_user1@example.com", password="secret")
        index_page_url = reverse('notes:index')
        response = self.client.get(index_page_url)
        notes = response.context["latest_note_list"]
        self.assertEquals(len(notes), self.paginate_by)

        pub_date = notes[0].pub_date
        for note in notes[1:]:
            self.assertTrue(pub_date >= note.pub_date)
            pub_date = note.pub_date

    def test_only_owned_notes_in_list(self):
        self.client.login(email="test_user2@example.com", password="secret")
        index_page_url = reverse('notes:index')
        response = self.client.get(index_page_url)
        notes = response.context["latest_note_list"]
        self.assertEquals(len(notes), 0)

    def test_pagination_is_five(self):
        self.client.login(email="test_user1@example.com", password="secret")
        index_page_url = reverse('notes:index')
        response = self.client.get(index_page_url)
        notes = response.context["latest_note_list"]
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEquals(len(notes), self.paginate_by)


class DetailTests(TestCase):

    def setUp(self):
        self.test_user1 = User.objects.create_user(
            email="test_user1@example.com",
            password="secret")
        self.test_user2 = User.objects.create_user(
            email="test_user2@example.com",
            password="secret")
        self.note = Note.objects.create(
            title="Note title", body="Note description", owner=self.test_user1)

    def test_redirect_if_not_logged_in(self):
        detail_page_url = reverse('notes:detail', kwargs={'pk': self.note.pk})
        response = self.client.get(detail_page_url)
        self.assertRedirects(response, f"/accounts/login/?next=/notes/{self.note.pk}/")

    def test_detail_view_status_code(self):
        self.client.login(email="test_user1@example.com", password="secret")
        url = reverse('notes:detail', kwargs={'pk': self.note.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_detail_url_resolves_detail_view(self):
        view = resolve(f'/notes/{self.note.pk}/')
        self.assertEquals(view.func.view_class, NoteDetail)

    def test_only_owner_can_see_detail_page(self):
        self.client.login(email="test_user2@example.com", password="secret")
        url = reverse('notes:detail', kwargs={'pk': self.note.pk})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

