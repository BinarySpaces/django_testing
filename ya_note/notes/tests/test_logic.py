from http import HTTPStatus
from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING
from .utils import (
    TestBaseClass,
    NOTES_ADD_URL,
    LOGIN_URL,
    NOTES_SUCCESS_URL,
    DELETE_SLUG_URL,
    EDIT_SLUG_URL,
)


FORM_DATA = {
    'title': 'title',
    'text': 'notetext',
    'slug': 'noteslug'
}


class TestNoteLogic(TestBaseClass):

    def test_slug_unique(self):
        note_count = Note.objects.count()
        FORM_DATA['slug'] = self.note.slug
        response = self.auth_author.post(NOTES_ADD_URL, data=FORM_DATA)
        form = response.context['form']
        self.assertFormError(
            response,
            form,
            'slug',
            errors=[self.note.slug + WARNING]
        )
        self.assertEqual(Note.objects.count(), note_count)

    def test_empty_slug(self):
        Note.objects.all().delete()
        FORM_DATA.pop('slug')
        response = self.auth_author.post(NOTES_ADD_URL, data=FORM_DATA)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(
            FORM_DATA['title'][:Note._meta.get_field('title').max_length])
        self.assertEqual(new_note.slug, expected_slug)

    def test_auth_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.auth_author.post(NOTES_ADD_URL, data=FORM_DATA)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.title, FORM_DATA['title'])
        self.assertEqual(note.text, FORM_DATA['text'])
        self.assertEqual(note.slug, FORM_DATA['slug'])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        note_count = Note.objects.count()
        response = self.client.post(NOTES_ADD_URL, data=FORM_DATA)
        expected_url = f'{LOGIN_URL}?next={NOTES_ADD_URL}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), note_count)

    def test_author_can_delete_note(self):
        response = self.auth_author.delete(DELETE_SLUG_URL)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_other_user_cant_delete_note(self):
        response = self.auth_other_user.post(DELETE_SLUG_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())

    def test_author_can_edit_note(self):
        response = self.auth_author.post(EDIT_SLUG_URL, data=FORM_DATA)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.text, FORM_DATA['text'])
        self.assertEqual(note.slug, FORM_DATA['slug'])
        self.assertEqual(note.title, FORM_DATA['title'])
        self.assertEqual(note.author, self.note.author)

    def test_other_user_cant_edit_note(self):
        response = self.auth_other_user.post(EDIT_SLUG_URL, data=FORM_DATA)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)
