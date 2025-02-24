from notes.forms import NoteForm

from .utils import (
    TestBaseClass,
    NOTES_LIST_URL,
    EDIT_SLUG_URL,
    NOTES_ADD_URL
)


class TestNotesList(TestBaseClass):

    def test_author_can_see_their_note_in_list(self):
        notes = self.auth_author.get(NOTES_LIST_URL).context['object_list']
        self.assertIn(self.note, notes)
        note = notes.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_other_users_cannot_see_author_notes(self):
        self.assertNotIn(
            self.note,
            self.auth_other_user.get(NOTES_LIST_URL).context['object_list']
        )

    def test_forms_are_available_for_author(self):
        urls = (
            NOTES_ADD_URL,
            EDIT_SLUG_URL
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.auth_author.get(url).context.get('form'), NoteForm
                )
