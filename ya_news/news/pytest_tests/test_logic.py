from http import HTTPStatus
import uuid

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.models import Comment


pytestmark = pytest.mark.django_db

FORM_DATA = {'text': 'Comment text'}
BAD_WORDS = ('редиска', 'негодяй')
WARNING = 'Не ругайтесь!'


def test_anonymous_user_cant_create_comment(
        client,
        news_detail,
        redirect_url_anonymous_user_comments,
):
    before_response_comments = list(Comment.objects.values(
        'id',
        'text',
        'news',
        'author',
        'created'
    ))
    response = client.post(news_detail, data=FORM_DATA)
    assertRedirects(response, redirect_url_anonymous_user_comments)
    assert before_response_comments == list(Comment.objects.values(
        'id',
        'text',
        'news',
        'author',
        'created'
    ))


def test_auth_user_can_create_comment(
        author_client,
        author,
        news_detail,
        news,
        redirect_url_auth_user_comments,
):
    unique_text = f"{FORM_DATA['text']} {uuid.uuid4()}"
    form_data = {**FORM_DATA, 'text': unique_text}

    before_response_comment_count = Comment.objects.count()
    response = author_client.post(news_detail, data=form_data)
    after_response_comment_count = Comment.objects.count()

    assertRedirects(response, redirect_url_auth_user_comments)
    assert after_response_comment_count == before_response_comment_count + 1

    new_comment = Comment.objects.get(text=unique_text)
    assert new_comment.text == form_data['text']
    assert new_comment.news == news
    assert new_comment.author == author


@pytest.mark.parametrize(
    'bad_word',
    BAD_WORDS,
)
def test_user_cant_use_bad_words(author_client, news_detail, bad_word):
    original_comments = list(Comment.objects.values(
        'id',
        'text',
        'news',
        'author',
        'created'
    ))
    response = author_client.post(news_detail, data={'text': bad_word})
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert original_comments == list(Comment.objects.values(
        'id',
        'text',
        'news',
        'author',
        'created'
    ))


def test_author_can_edit_comment(
        author_client,
        comment,
        comment_edit,
        redirect_url_auth_user_comments,
):
    original_author = comment.author
    original_news = comment.news
    response = author_client.post(comment_edit, data=FORM_DATA)
    assertRedirects(response, redirect_url_auth_user_comments)
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == FORM_DATA['text']
    assert updated_comment.author == original_author
    assert updated_comment.news == original_news


def test_author_can_delete_comment(
        author_client,
        comment,
        comment_delete,
        redirect_url_auth_user_comments,
):
    count_before_delete = Comment.objects.count()
    response = author_client.post(comment_delete)
    assertRedirects(response, redirect_url_auth_user_comments)
    count_after_delete = Comment.objects.count()
    assert count_before_delete - 1 == count_after_delete
    assert not Comment.objects.filter(pk=comment.id).exists()


def test_other_cant_edit_comment(
        not_author_client,
        comment,
        comment_edit,
):
    response = not_author_client.post(comment_edit, data=FORM_DATA)
    updated_comment = Comment.objects.get(id=comment.id)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == updated_comment.text
    assert comment.news == updated_comment.news
    assert comment.author == updated_comment.author


def test_other_cant_delete_comment(
        not_author_client,
        comment,
        comment_delete,
):
    response = not_author_client.post(comment_delete)
    updated_comment = Comment.objects.get(pk=comment.id)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(pk=comment.id).exists()
    assert comment.text == updated_comment.text
    assert comment.news == updated_comment.news
    assert comment.author == updated_comment.author
