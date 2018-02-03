from django.test import TestCase
from django.urls import reverse, resolve

from notes.models import Note
from notes.views import index, detail


class IndexTests(TestCase):

    def setUp(self):
        self.note = Note.objects.create(
            title="Note title", body="Note description")
        url = reverse('notes:index')
        self.response = self.client.get(url)

    def test_index_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_index_url_resolves_index_view(self):
        view = resolve('/notes/')
        self.assertEquals(view.func, index)

    def test_index_view_contains_link_to_details_page(self):
        note_detail_url = reverse('notes:detail', kwargs={
            'note_id': self.note.pk})
        self.assertContains(self.response, f'href="{note_detail_url}"')


class DetailTests(TestCase):

    def setUp(self):
        self.note = Note.objects.create(
            title="Note title", body="Note description")
        url = reverse('notes:detail', kwargs={'note_id': self.note.pk})
        self.response = self.client.get(url)

    def test_detail_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_detail_url_resolves_detail_view(self):
        view = resolve(f'/notes/{self.note.pk}/')
        self.assertEquals(view.func, detail)

