from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .utils import (
    TestBaseClass,
    NOTES_ADD_URL,
    NOTES_SUCCESS_URL,
    DELETE_SLUG_URL,
    EDIT_SLUG_URL,
    REDIRECT_NOTES_ADD_URL
)


class TestNoteLogic(TestBaseClass):

    def test_slug_unique(self):
        before_response_notes = list(Note.objects.values(
            'id', 'title', 'text', 'slug', 'author',
        ))
        self.form_data['slug'] = self.note.slug
        response = self.auth_author.post(NOTES_ADD_URL, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=self.note.slug + WARNING
        )
        self.assertCountEqual(
            before_response_notes,
            list(Note.objects.values('id', 'title', 'text', 'slug', 'author',))
        )

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.auth_author.post(NOTES_ADD_URL, data=self.form_data)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)

        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, slugify(self.form_data['title']))
        self.assertEqual(note.author, self.author)

    def test_auth_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.auth_author.post(NOTES_ADD_URL, data=self.FORM_DATA)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)

        note = Note.objects.get()
        self.assertEqual(note.title, self.FORM_DATA['title'])
        self.assertEqual(note.text, self.FORM_DATA['text'])
        self.assertEqual(note.slug, self.FORM_DATA['slug'])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        before_response_notes = list(Note.objects.values(
            'id', 'title', 'text', 'slug', 'author',
        ))
        response = self.client.post(NOTES_ADD_URL, data=self.FORM_DATA)
        self.assertRedirects(response, REDIRECT_NOTES_ADD_URL)
        self.assertCountEqual(
            before_response_notes,
            list(Note.objects.values('id', 'title', 'text', 'slug', 'author',))
        )

    def test_author_can_delete_note(self):
        note_count = Note.objects.count()
        response = self.auth_author.delete(DELETE_SLUG_URL)
        self.assertRedirects(response, NOTES_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), note_count - 1)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_other_user_cant_delete_note(self):
        response = self.auth_other_user.post(DELETE_SLUG_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())

        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_author_can_edit_note(self):
        response = self.auth_author.post(EDIT_SLUG_URL, data=self.FORM_DATA)
        self.assertRedirects(response, NOTES_SUCCESS_URL)

        note = Note.objects.get(pk=self.note.pk)
        self.assertEqual(note.text, self.FORM_DATA['text'])
        self.assertEqual(note.slug, self.FORM_DATA['slug'])
        self.assertEqual(note.title, self.FORM_DATA['title'])
        self.assertEqual(note.author, self.note.author)

    def test_other_user_cant_edit_note(self):
        response = self.auth_other_user.post(
            EDIT_SLUG_URL,
            data=self.FORM_DATA
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)
