import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, news_home):
    assert len(
        client.get(news_home).context['object_list']
    ) <= settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_date_order(client, news_home):
    all_dates = [
        news.date for news in client.get(news_home).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_sorted(client, news_detail):
    response = client.get(news_detail)
    all_comments = response.context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    assert all_timestamps == sorted(all_timestamps)


def test_comment_form_for_anonym(client, news_detail):
    response = client.get(news_detail)
    context = response.context
    assert 'form' not in context


def test_comment_form_for_login_user(author_client, news_detail):
    response = author_client.get(news_detail)
    context = response.context
    assert 'form' in context
    assert isinstance(context['form'], CommentForm)
