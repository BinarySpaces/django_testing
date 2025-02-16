from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(
        client,
        news_detail,
        login,
        form_data
):
    before_comment_count = Comment.objects.count()
    response = client.post(news_detail, data=form_data)
    after_comment_count = Comment.objects.count()
    assertRedirects(response, f'{login}?next={news_detail}')
    assert before_comment_count == after_comment_count


def test_auth_user_can_create_comment(
        author_client,
        author,
        news_detail,
        form_data,
        comment,
        news
):
    before_comment_count = Comment.objects.count()
    response = author_client.post(news_detail, data=form_data)
    after_comment_count = Comment.objects.count()
    assertRedirects(response, news_detail + '#comments')
    assert after_comment_count - 1 == before_comment_count
    new_comment = Comment.objects.latest('id')
    assert new_comment.text == form_data['text']
    assert new_comment.news == news
    assert new_comment.author == author


def test_user_cant_use_bad_words(author_client, news_detail):
    bad_word_text = {
        'text': BAD_WORDS[0]
    }
    before_comment_count = Comment.objects.count()
    response = author_client.post(news_detail, data=bad_word_text)
    form = response.context['form']
    after_comment_count = Comment.objects.count()
    assertFormError(form, 'text', [WARNING])
    assert before_comment_count == after_comment_count


def test_author_can_edit_comment(
        author_client,
        comment,
        form_data,
        comment_edit,
        news_detail,
        author,
        news
):
    response = author_client.post(comment_edit, data=form_data)
    assertRedirects(response, news_detail + '#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']
    assert comment.author == author
    assert comment.news == news


def test_author_can_delete_comment(
        author_client,
        comment,
        comment_delete,
        news_detail
):
    count_before_delete = Comment.objects.count()
    response = author_client.post(comment_delete)
    assertRedirects(response, news_detail + '#comments')
    count_after_delete = Comment.objects.count()
    assert count_before_delete - 1 == count_after_delete
    assert not Comment.objects.filter(pk=comment.id).exists()


def test_other_cant_edit_comment(
        not_author_client,
        comment,
        comment_edit,
        form_data
):
    response = not_author_client.post(comment_edit, data=form_data)
    comment_text = Comment.objects.get(id=comment.id)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == comment_text.text
    assert comment.news == comment_text.news
    assert comment.author == comment_text.author


def test_other_cant_delete_comment(
        not_author_client,
        comment,
        comment_delete
):
    response = not_author_client.post(comment_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.filter(pk=comment.id).exists()
