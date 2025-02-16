import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, news_home, create_bulk_of_news):
    response = client.get(news_home)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count <= settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_date_order(client, news_home, create_bulk_of_news):
    response = client.get(news_home)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_sorted(client, news_detail, create_bulk_of_comments):
    response = client.get(news_detail)
    all_comments = response.context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_comment_form_for_anonym(news, client, news_detail):
    response = client.get(news_detail)
    context = response.context
    assert 'form' not in context


def test_comment_form_for_login_user(news, author_client, news_detail):
    response = author_client.get(news_detail)
    context = response.context
    assert 'form' in context
    assert isinstance(context['form'], CommentForm)
