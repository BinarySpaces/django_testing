from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db

BAD_WORDS_FORM_DATA = [{'text': word} for word in BAD_WORDS]
FORM_DATA = {'text': 'Comment text'}


def test_anonymous_user_cant_create_comment(
        client,
        news_detail,
        redirect_url_anonymous_user_comments,
):
    before_response_comments = set(  # Отличное решение!
        Comment.objects.values_list('id', flat=True)
    )
    response = client.post(news_detail, data=FORM_DATA)
    assertRedirects(response, redirect_url_anonymous_user_comments)
    assert (
        before_response_comments
        == set(Comment.objects.values_list('id', flat=True))
    )


def test_auth_user_can_create_comment(
        author_client,
        author,
        news_detail,
        news,
        redirect_url_auth_user_comments,
):
    response = author_client.post(news_detail, data=FORM_DATA)

    assertRedirects(response, redirect_url_auth_user_comments)
    assert Comment.objects.count() == 1

    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize(
    'form_data',
    BAD_WORDS_FORM_DATA,
)
def test_user_cant_use_bad_words(author_client, news_detail, form_data):
    original_comments = set(
        Comment.objects.values_list('id', flat=True)
    )
    response = author_client.post(news_detail, data=form_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert (
        original_comments
        == set(Comment.objects.values_list('id', flat=True))
    )


def test_author_can_edit_comment(
        author_client,
        comment,
        comment_edit,
        redirect_url_auth_user_comments,
):
    response = author_client.post(comment_edit, data=FORM_DATA)
    assertRedirects(response, redirect_url_auth_user_comments)
    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.text == FORM_DATA['text']
    assert updated_comment.author == comment.author
    assert updated_comment.news == comment.news


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
    assert Comment.objects.filter(pk=comment.id).exists()
    updated_comment = Comment.objects.get(pk=comment.id)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == updated_comment.text
    assert comment.news == updated_comment.news
    assert comment.author == updated_comment.author
