from django.test import TestCase

from notes.models import Note


class TestNoteModel(TestCase):

    def test_can_create_a_new_note(self):
        note = Note.objects.create(title='Note title', body='Note body')
        self.assertTrue(note)

    def test_string_representation(self):
        note = Note.objects.create(title='Note title', body='Note body')
        self.assertEqual(str(note), 'Note title')

