from django.test import TestCase
from django.utils import timezone

from notes.models import Note


class TestNoteModel(TestCase):

    def test_can_create_a_new_note(self):
        note = Note.objects.create(title='Note title', body='Note body')
        self.assertTrue(note)

    def test_string_representation(self):
        note = Note.objects.create(title='Note title', body='Note body')
        self.assertEqual(str(note), 'Note title')

    def test_was_published_recently(self):
        time = timezone.now() + timezone.timedelta(days=30)
        future_note = Note(pub_date=time)
        self.assertEqual(future_note.was_published_recently(), False)

