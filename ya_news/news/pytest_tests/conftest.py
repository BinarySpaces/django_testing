from datetime import datetime, timedelta

from django.conf import settings
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone
import pytest

from news.models import News, Comment


@pytest.fixture
def all_urls(
    login,
    logout,
    signup,
    news_home,
    news_detail,
    comment_edit,
    comment_delete
):
    return {
        'login': login,
        'logout': logout,
        'signup': signup,
        'news_home': news_home,
        'news_detail': news_detail,
        'comment_edit': comment_edit,
        'comment_delete': comment_delete,
    }


@pytest.fixture
def all_clients(author_client, not_author_client):
    return {
        'author': author_client,
        'not_author': not_author_client,
        'client': Client(),
    }


@pytest.fixture
def redirect_urls(redirect_url_edit_comment, redirect_url_delete_comment):
    return {
        'redirect_url_edit_comment': redirect_url_edit_comment,
        'redirect_url_delete_comment': redirect_url_delete_comment,
    }


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
    return f'{news_detail}#comments'


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
