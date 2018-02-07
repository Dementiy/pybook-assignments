from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from notes.models import Note

User = get_user_model()

class NoteViewTest(TestCase):

    def setUp(self):
        self.test_user1 = User.objects.create_user(
            email="test_user1@example.com",
            password="secret")
        self.test_user2 = User.objects.create_user(
            email="test_user2@example.com",
            password="secret")

        self.n = 5
        self.notes = []
        for i in range(self.n):
            self.notes.append(Note.objects.create(
                title=f"Note title {i}",
                body="Note body",
                owner=self.test_user1))

        self.test_user2_note = Note.objects.create(
            title="Note title",
            body="Note body",
            owner=self.test_user2)

        self.client = APIClient()

    def _authenticate(self):
        response = self.client.post('/api/jwt-auth/', {
            "email": "test_user1@example.com",
            "password": "secret"
        }, format="json")
        token = response.json()["token"]
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def test_api_can_get_note_list(self):
        self._authenticate()
        response = self.client.get(reverse('api:note-list'))
        self.assertEquals(len(response.json()), self.n)

    def test_api_can_get_note_detail(self):
        self._authenticate()
        pk = self.notes[0].id
        response = self.client.get(reverse('api:note-detail', kwargs={"pk": pk}))
        note = response.json()
        self.assertEquals(note["id"], self.notes[0].id)
        self.assertEquals(note["title"], self.notes[0].title)
        self.assertEquals(note["body"], self.notes[0].body)

    def test_api_can_create_note(self):
        self._authenticate()
        response = self.client.post(reverse('api:note-list'),
            {
                "title": "New note title",
                "body": "New note body"
            }, format="json")
        note = Note.objects.filter(owner=self.test_user1).last()
        self.assertEquals(Note.objects.filter(owner=self.test_user1).count(),
            self.n + 1)
        self.assertEquals(note.title, "New note title")
        self.assertEquals(note.body, "New note body")

    def test_api_can_update_note(self):
        self._authenticate()
        pk = self.notes[0].id
        response = self.client.put(reverse('api:note-detail', kwargs={"pk": pk}),
            {
                "title": "Note title updated",
                "body": "Note body updated"
            }, format="json")
        note = Note.objects.get(pk=pk)
        self.assertEquals(note.title, "Note title updated")
        self.assertEquals(note.body, "Note body updated")

    def test_api_can_delete_note(self):
        self._authenticate()
        pk = self.notes[0].id
        response = self.client.delete(reverse('api:note-detail', kwargs={"pk": pk}))
        self.assertEquals(Note.objects.filter(owner=self.test_user1).count(),
            self.n-1)

    def test_api_only_owner_can_get_note_detail(self):
        self._authenticate()
        response = self.client.get(reverse('api:note-detail',
            kwargs={"pk": self.test_user2_note.id}))
        self.assertEquals(response.json()["detail"], "Not found.")

    def test_api_only_owner_can_update_note(self):
        self._authenticate()
        pk = self.test_user2_note.id
        response = self.client.put(reverse('api:note-detail', kwargs={"pk": pk}),
            {
                "title": "Note title updated",
                "body": "Note body updated"
            }, format="json")
        note = Note.objects.get(pk=pk)
        self.assertEquals(response.json()["detail"], "Not found.")
        self.assertEquals(note.title, "Note title")
        self.assertEquals(note.body, "Note body")

    def test_api_only_owner_can_delete_note(self):
        self._authenticate()
        pk = self.test_user2_note.id
        response = self.client.delete(reverse('api:note-detail', kwargs={"pk": pk}))
        self.assertEquals(response.json()["detail"], "Not found.")
        self.assertEquals(Note.objects.filter(owner=self.test_user2).count(), 1)

