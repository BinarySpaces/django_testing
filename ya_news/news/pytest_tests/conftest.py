from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from news.models import News, Comment


CLIENT = Client()
NEWS_HOME_URL = ''
NEWS_DETAIL_URL = '/news/1/'
NEWS_LOGIN_URL = '/auth/login/'
NEWS_LOGOUT_URL = '/auth/logout/'
NEWS_SIGNUP_URL = '/auth/signup/'
COMMENT_EDIT_URL = '/edit_comment/1/'
COMMENT_DELETE_URL = '/delete_comment/1/'
REDIRECT_URL_EDIT_COMMENT = '/auth/login/?next=/edit_comment/1/'
REDIRECT_URL_DELETE_COMMENT = '/auth/login/?next=/delete_comment/1/'

@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Autor')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Not autor')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='News title',
        text='News text',
    )


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Comment text'
    )


@pytest.fixture
def redirect_url_anonymous_user_comments(login, news_detail):
    return f'{login}?next={news_detail}'


@pytest.fixture
def redirect_url_auth_user_comments(news_detail):
    return news_detail + '#comments'


@pytest.fixture
def news_detail(news):
    return reverse('news:detail', args=[news.pk])


@pytest.fixture
def news_home():
    return reverse('news:home')


@pytest.fixture
def comment_edit(comment):
    return reverse('news:edit', args=[comment.pk])


@pytest.fixture
def comment_delete(comment):
    return reverse('news:delete', args=[comment.pk])


@pytest.fixture
def redirect_url_edit_comment(login, comment_edit):
    return f'{login}?next={comment_edit}'


@pytest.fixture
def redirect_url_delete_comment(login, comment_delete):
    return f'{login}?next={comment_delete}'


@pytest.fixture
def login():
    return reverse('users:login')


@pytest.fixture
def logout():
    return reverse('users:logout')


@pytest.fixture
def signup():
    return reverse('users:signup')


@pytest.fixture
def bulk_of_news():
    News.objects.bulk_create(
        News(title=f'News number {index}',
             text='News text',
             date=datetime.today() - timedelta(days=index)
             )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def bulk_of_comments(news, author):
    now = timezone.now()
    for index in range(3):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Comment text number {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
