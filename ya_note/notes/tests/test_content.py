from notes.forms import NoteForm

from .utils import (
    TestBaseClass,
    NOTES_LIST_URL,
    EDIT_SLUG_URL,
    NOTES_ADD_URL
)


class TestNotesList(TestBaseClass):

    def test_note_in_list(self):
        response = self.auth_author.get(NOTES_LIST_URL)
        notes_queryset = response.context['object_list']
        self.assertIn(self.note, notes_queryset)

    def test_notes_do_not_mix_for_author(self):
        response = self.auth_other_user.get(NOTES_LIST_URL)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_existing_form(self):
        urls = (
            NOTES_ADD_URL,
            EDIT_SLUG_URL
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_author.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
