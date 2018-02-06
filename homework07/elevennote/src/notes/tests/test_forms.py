from django.test import TestCase
from django.contrib.auth import get_user_model

from notes.models import Note
from notes.forms import NoteForm


User = get_user_model()

class NoteFormTests(TestCase):

    def test_form_save(self):
        data = {'title': 'Note Title', 'body': 'Note body'}
        form = NoteForm(data=data)
        self.assertTrue(form.is_valid())

        user = User.objects.create_user(email='user@example.com', password='secret')
        form.instance.owner = user
        note = form.save()
        self.assertEqual(note, Note.objects.first())

