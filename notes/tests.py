from django.test import TestCase
from django.urls import reverse
from .models import Note

class NoteTests(TestCase):

    def setUp(self):
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note."
        )

    def test_note_list_view(self):
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.note.title)

    def test_note_create_view(self):
        response = self.client.post(reverse('note_create'), {
            'title': 'New Note',
            'content': 'Some new note content'
        })
        self.assertEqual(response.status_code, 302)  # redirect after creation
        self.assertEqual(Note.objects.last().title, 'New Note')

    def test_note_update_view(self):
        response = self.client.post(reverse('note_update', args=[self.note.id]), {
            'title': 'Updated Title',
            'content': 'Updated Content',
        })

        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Title')

    def test_note_delete_view(self):
        response = self.client.post(reverse('note_delete', args=[self.note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
