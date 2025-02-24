from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_key, client_method, expected_status, expected_redirect_fixture',
    (
        ('login', 'author.get', HTTPStatus.OK, None),
        ('logout', 'author.post', HTTPStatus.OK, None),
        ('signup', 'author.get', HTTPStatus.OK, None),
        ('news_home', 'author.get', HTTPStatus.OK, None),
        ('news_detail', 'author.get', HTTPStatus.OK, None),
        ('comment_edit', 'author.get', HTTPStatus.OK, None),
        ('comment_delete', 'author.get', HTTPStatus.OK, None),
        ('comment_edit', 'not_author.get', HTTPStatus.NOT_FOUND, None),
        ('comment_delete', 'not_author.get', HTTPStatus.NOT_FOUND, None),
        (
            'comment_edit',
            'client.get',
            HTTPStatus.FOUND,
            'redirect_url_edit_comment'
        ),
        (
            'comment_delete',
            'client.get',
            HTTPStatus.FOUND,
            'redirect_url_delete_comment'
        ),
    )
)
def test_pages_availability_for_users(
    all_urls,
    all_clients,
    redirect_urls,
    url_key,
    client_method,
    expected_status,
    expected_redirect_fixture,
):
    client, method = client_method.split('.')
    response = getattr(
        all_clients[client],
        method
    )(all_urls[url_key])

    assert response.status_code == expected_status
    if expected_redirect_fixture is not None:
        redirect_url = redirect_urls[expected_redirect_fixture]
        assert response.url == redirect_url


@pytest.mark.parametrize(
    'url_key, client, expected_redirect_fixture',
    (
        ('comment_edit', 'client', 'redirect_url_edit_comment'),
        ('comment_delete', 'client', 'redirect_url_delete_comment'),
    ),
)
def test_redirects(
    all_urls,
    all_clients,
    redirect_urls,
    url_key,
    client,
    expected_redirect_fixture,
):
    assertRedirects(
        all_clients[client].get(all_urls[url_key]),
        redirect_urls[expected_redirect_fixture],
        status_code=HTTPStatus.FOUND,
        target_status_code=HTTPStatus.OK,
    )
