from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from .conftest import (
    CLIENT,
    NEWS_HOME_URL,
    NEWS_DETAIL_URL,
    NEWS_LOGIN_URL,
    NEWS_LOGOUT_URL,
    NEWS_SIGNUP_URL,
    COMMENT_EDIT_URL,
    COMMENT_DELETE_URL,
    REDIRECT_URL_EDIT_COMMENT,
    REDIRECT_URL_DELETE_COMMENT,
)


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, client_or_method, expected_status, expected_redirect',
    (
        (NEWS_LOGIN_URL, CLIENT.get, HTTPStatus.OK, None),
        (NEWS_LOGOUT_URL, CLIENT.post, HTTPStatus.OK, None),
        (NEWS_SIGNUP_URL, CLIENT.get, HTTPStatus.OK, None),
        (NEWS_HOME_URL, CLIENT.get, HTTPStatus.OK, None),
        (NEWS_DETAIL_URL, CLIENT.get, HTTPStatus.OK, None),
        (COMMENT_EDIT_URL, 'author_client', HTTPStatus.OK, None),
        (COMMENT_EDIT_URL, 'not_author_client', HTTPStatus.NOT_FOUND, None),
        (COMMENT_DELETE_URL, 'author_client', HTTPStatus.OK, None),
        (COMMENT_DELETE_URL, 'not_author_client', HTTPStatus.NOT_FOUND, None),
        (
            COMMENT_EDIT_URL,
            CLIENT.get,
            HTTPStatus.FOUND,
            REDIRECT_URL_EDIT_COMMENT
        ),
        (
            COMMENT_DELETE_URL,
            CLIENT.get,
            HTTPStatus.FOUND,
            REDIRECT_URL_DELETE_COMMENT
        ),
    ),
)
def test_pages_availability_for_users(
    request,
    url,
    client_or_method,
    expected_status,
    expected_redirect,
    comment,
    news
):
    news = news
    comment = comment

    if isinstance(client_or_method, str):
        client = request.getfixturevalue(client_or_method)
        method = client.get
    else:
        method = client_or_method
    response = method(url)

    assert response.status_code == expected_status
    if expected_redirect:
        assert response.url == expected_redirect


@pytest.mark.parametrize(
    'url, user, expected_redirect',
    (
        (COMMENT_EDIT_URL, CLIENT, REDIRECT_URL_EDIT_COMMENT),
        (COMMENT_DELETE_URL, CLIENT, REDIRECT_URL_DELETE_COMMENT),
    ),

)
def test_redirects(url, user, expected_redirect):
    assertRedirects(user.get(url), expected_redirect)
