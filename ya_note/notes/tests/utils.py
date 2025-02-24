from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note, User


SLUG = 'details'
NOTES_HOME_URL = reverse('notes:home')
NOTES_LIST_URL = reverse('notes:list')
NOTES_ADD_URL = reverse('notes:add')
NOTES_SUCCESS_URL = reverse('notes:success')
SIGN_UP_URL = reverse('users:signup')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
LOGIN_REDIRECT_TEMPLATE = f'{LOGIN_URL}?next='
DETAIL_SLUG_URL = reverse('notes:detail', args=(SLUG,))
EDIT_SLUG_URL = reverse('notes:edit', args=(SLUG,))
DELETE_SLUG_URL = reverse('notes:delete', args=(SLUG,))
REDIRECT_EDIT_SLUG_URL = f'{LOGIN_REDIRECT_TEMPLATE}{EDIT_SLUG_URL}'
REDIRECT_DELETE_SLUG_URL = f'{LOGIN_REDIRECT_TEMPLATE}{DELETE_SLUG_URL}'
REDIRECT_DETAIL_SLUG_URL = f'{LOGIN_REDIRECT_TEMPLATE}{DETAIL_SLUG_URL}'
REDIRECT_NOTES_LIST_URL = f'{LOGIN_REDIRECT_TEMPLATE}{NOTES_LIST_URL}'
REDIRECT_NOTES_ADD_URL = f'{LOGIN_REDIRECT_TEMPLATE}{NOTES_ADD_URL}'
REDIRECT_NOTES_SUCCESS_URL = f'{LOGIN_REDIRECT_TEMPLATE}{NOTES_SUCCESS_URL}'


class TestBaseClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.other_user = User.objects.create(username='Reader')
        cls.auth_author = Client()
        cls.auth_other_user = Client()
        cls.auth_author.force_login(cls.author)
        cls.auth_other_user.force_login(cls.other_user)
        cls.note = Note.objects.create(
            title='Название заметки',
            text='Подробности',
            slug=SLUG,
            author=cls.author
        )
        cls.form_data = {
            'title': 'title',
            'text': 'notetext',
            'slug': 'noteslug'
        }
