from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from django.test.client import Client


pytestmark = pytest.mark.django_db

CLIENT = Client()

AUTHOR_ONLY_ROUTES = (
    'comment_edit',
    'comment_delete',
)


@pytest.mark.parametrize(
    'url_fixture, client_method, expected_status',
    (
        ('login', 'get', HTTPStatus.OK),
        ('logout', 'post', HTTPStatus.OK),
        ('signup', 'get', HTTPStatus.OK),
        ('news_home', 'get', HTTPStatus.OK),
        ('news_detail', 'get', HTTPStatus.OK),
        ('comment_edit', 'get', HTTPStatus.OK),
        ('comment_edit', 'get', HTTPStatus.NOT_FOUND),
        ('comment_delete', 'get', HTTPStatus.OK),
        ('comment_delete', 'get', HTTPStatus.NOT_FOUND),
    )
)
def test_pages_availability_for_users_without_redirect(
    request,
    url_fixture,
    client_method,
    expected_status,
    author_client,
    not_author_client,
    comment,
    news,
):
    news = news
    comment = comment

    client = (
        author_client
        if url_fixture in AUTHOR_ONLY_ROUTES
        and expected_status == HTTPStatus.OK
        else not_author_client
    )
    response = getattr(client, client_method)(
        request.getfixturevalue(url_fixture)
    )
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    (
        'url_fixture',
        'client_method',
        'expected_status',
        'expected_redirect_fixture',
    ),
    (
        (
            'comment_edit',
            CLIENT.get,
            HTTPStatus.FOUND,
            'redirect_url_edit_comment'
        ),
        (
            'comment_delete',
            CLIENT.get,
            HTTPStatus.FOUND,
            'redirect_url_delete_comment'
        ),
    ),
)
def test_pages_availability_for_users_with_redirect(
    request,
    url_fixture,
    client_method,
    expected_status,
    expected_redirect_fixture,
):
    response = client_method(request.getfixturevalue(url_fixture))
    assert response.status_code == expected_status
    assert response.url == request.getfixturevalue(expected_redirect_fixture)


@pytest.mark.parametrize(
    'url_fixture, user, expected_redirect_fixture',
    (
        ('comment_edit', CLIENT, 'redirect_url_edit_comment'),
        ('comment_delete', CLIENT, 'redirect_url_delete_comment'),
    ),
)
def test_redirects(request, url_fixture, user, expected_redirect_fixture,):
    assertRedirects(
        user.get(request.getfixturevalue(url_fixture)),
        request.getfixturevalue(expected_redirect_fixture)
    )
