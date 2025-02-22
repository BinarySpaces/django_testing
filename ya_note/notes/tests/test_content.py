from notes.forms import NoteForm

from .utils import (
    TestBaseClass,
    NOTES_LIST_URL,
    EDIT_SLUG_URL,
    NOTES_ADD_URL
)


class TestNotesList(TestBaseClass):

    def test_note_in_list(self):
        notes = self.auth_author.get(NOTES_LIST_URL).context['object_list']
        self.assertIn(self.note, notes)
        note_in_list = next(
            (note for note in notes if note.id == self.note.id), None
        )
        self.assertIsNotNone(note_in_list)
        self.assertEqual(note_in_list.title, self.note.title)
        self.assertEqual(note_in_list.text, self.note.text)
        self.assertEqual(note_in_list.slug, self.note.slug)
        self.assertEqual(note_in_list.author, self.note.author)

    def test_notes_do_not_mix_for_author(self):
        self.assertNotIn(
            self.note,
            self.auth_other_user.get(NOTES_LIST_URL).context['object_list']
        )

    def test_existing_form(self):
        urls = (
            NOTES_ADD_URL,
            EDIT_SLUG_URL
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.auth_author.get(url).context.get('form'), NoteForm
                )
