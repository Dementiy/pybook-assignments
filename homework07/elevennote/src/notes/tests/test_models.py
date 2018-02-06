from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from notes.models import Note


User = get_user_model()

class TestNoteModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='secret'
        )

    def test_can_create_a_new_note(self):
        note = Note.objects.create(title='Note title',
            body='Note body', owner=self.user)
        self.assertTrue(note)

    def test_string_representation(self):
        note = Note.objects.create(title='Note title',
            body='Note body', owner=self.user)
        self.assertEqual(str(note), 'Note title')

    def test_was_published_recently(self):
        time = timezone.now() + timezone.timedelta(days=30)
        future_note = Note(pub_date=time)
        self.assertEqual(future_note.was_published_recently(), False)

