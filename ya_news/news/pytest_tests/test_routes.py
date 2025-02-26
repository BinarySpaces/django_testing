from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db


CLIENT = pytest.lazy_fixture('client')
NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail')
NEWS_HOME_URL = pytest.lazy_fixture('news_home')
NEWS_LOGIN_URL = pytest.lazy_fixture('login')
NEWS_LOGOUT_URL = pytest.lazy_fixture('logout')
NEWS_SIGNUP_URL = pytest.lazy_fixture('signup')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
COMMENT_EDIT_URL = pytest.lazy_fixture('comment_edit')
COMMENT_DELETE_URL = pytest.lazy_fixture('comment_delete')
REDIRECT_URL_EDIT_COMMENT = pytest.lazy_fixture('redirect_url_edit_comment')
REDIRECT_URL_DELETE_COMMENT = (
    pytest.lazy_fixture('redirect_url_delete_comment')
)


@pytest.mark.parametrize(
    'url, user, expected_status',
    (
        (NEWS_LOGIN_URL, CLIENT, HTTPStatus.OK),
        (NEWS_LOGOUT_URL, CLIENT, HTTPStatus.OK),
        (NEWS_SIGNUP_URL, CLIENT, HTTPStatus.OK),
        (NEWS_DETAIL_URL, CLIENT, HTTPStatus.OK),
        (NEWS_HOME_URL, CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT_URL, CLIENT, HTTPStatus.FOUND),
        (COMMENT_DELETE_URL, CLIENT, HTTPStatus.FOUND),
        (COMMENT_EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (COMMENT_DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_DELETE_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability_for_users(url, user, expected_status):
    assert user.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, user, expected_redirect_fixture',
    (
        (COMMENT_EDIT_URL, CLIENT, REDIRECT_URL_EDIT_COMMENT),
        (COMMENT_DELETE_URL, CLIENT, REDIRECT_URL_DELETE_COMMENT),
    )
)
def test_redirects(url, user, expected_redirect_fixture):
    assertRedirects(user.get(url), expected_redirect_fixture)
