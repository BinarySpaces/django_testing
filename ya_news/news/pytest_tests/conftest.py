from datetime import datetime, timedelta
import pytest
from django.test.client import Client
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from news.models import News, Comment


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
    news = News.objects.create(
        title='News title',
        text='News text',
    )
    return news


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Comment text'
    )
    return comment


@pytest.fixture
def form_data():
    return {
        'text': 'Comment text'
    }


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
def redirect_url_edit_comment(comment, login):
    url = reverse('news:edit', args=[comment.pk])
    return f'{login}?next={url}'


@pytest.fixture
def redirect_url_delete_comment(comment, login):
    url = reverse('news:delete', args=[comment.pk])
    return f'{login}?next={url}'


@pytest.fixture
def login():
    return reverse('users:login')


@pytest.fixture
def logout():
    return reverse('users:login')


@pytest.fixture
def signup():
    return reverse('users:signup')


@pytest.fixture
def create_bulk_of_news():
    News.objects.bulk_create(
        News(title=f'News number {index}',
             text='News text',
             date=datetime.today() - timedelta(days=index)
             )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def create_bulk_of_comments(news, author):
    now = timezone.now()
    for index in range(3):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Comment text number {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
