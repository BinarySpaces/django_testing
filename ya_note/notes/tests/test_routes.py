from http import HTTPStatus

from .utils import (
    TestBaseClass,
    NOTES_ADD_URL,
    NOTES_SUCCESS_URL,
    DELETE_SLUG_URL,
    EDIT_SLUG_URL,
    DETAIL_SLUG_URL,
    NOTES_HOME_URL,
    NOTES_LIST_URL,
    LOGIN_URL,
    SIGN_UP_URL,
    LOGOUT_URL,
    REDIRECT_EDIT_SLUG_URL,
    REDIRECT_DELETE_SLUG_URL,
    REDIRECT_DETAIL_SLUG_URL,
    REDIRECT_NOTES_LIST_URL,
    REDIRECT_NOTES_ADD_URL,
    REDIRECT_NOTES_SUCCESS_URL,
)


class TestRoutes(TestBaseClass):

    def test_availability_for_pages(self):
        parametrized_options = (
            (DETAIL_SLUG_URL, self.auth_author.get, HTTPStatus.OK, None),
            (DETAIL_SLUG_URL, self.auth_other_user.get, HTTPStatus.NOT_FOUND, None),
            (EDIT_SLUG_URL, self.auth_author.get, HTTPStatus.OK, None),
            (EDIT_SLUG_URL, self.auth_other_user.get, HTTPStatus.NOT_FOUND, None),
            (EDIT_SLUG_URL, self.client.get, HTTPStatus.FOUND, REDIRECT_EDIT_SLUG_URL),
            (DELETE_SLUG_URL, self.auth_author.get, HTTPStatus.OK, None),
            (DELETE_SLUG_URL, self.auth_other_user.get, HTTPStatus.NOT_FOUND, None),
            (DELETE_SLUG_URL, self.client.get, HTTPStatus.FOUND, REDIRECT_DELETE_SLUG_URL),
            (NOTES_LIST_URL, self.auth_author.get, HTTPStatus.OK, None),
            (NOTES_ADD_URL, self.auth_author.get, HTTPStatus.OK, None),
            (NOTES_SUCCESS_URL, self.auth_author.get, HTTPStatus.OK, None),
            (NOTES_HOME_URL, self.client.get, HTTPStatus.OK, None),
            (LOGIN_URL, self.client.get, HTTPStatus.OK, None),
            (LOGOUT_URL, self.client.post, HTTPStatus.OK, None),
            (SIGN_UP_URL, self.client.get, HTTPStatus.OK, None),
        )
        for url, client_method, expected_status, expected_redirect in parametrized_options:
            with self.subTest(
                url=url,
                client_method=client_method,
                expected_status=expected_status,
                redirect=expected_redirect
            ):
                response = client_method(url)
                assert response.status_code == expected_status
                if expected_redirect:
                    assert response.url == expected_redirect

    def test_redirect_for_anonymous_client(self):
        parametrized_options = (
            (EDIT_SLUG_URL, self.client, REDIRECT_EDIT_SLUG_URL),
            (DELETE_SLUG_URL, self.client, REDIRECT_DELETE_SLUG_URL),
            (DETAIL_SLUG_URL, self.client, REDIRECT_DETAIL_SLUG_URL),
            (NOTES_LIST_URL, self.client, REDIRECT_NOTES_LIST_URL),
            (NOTES_ADD_URL, self.client, REDIRECT_NOTES_ADD_URL),
            (NOTES_SUCCESS_URL, self.client, REDIRECT_NOTES_SUCCESS_URL)
        )
        for url, user, redirect_url in parametrized_options:
            with self.subTest(url=url, user=user, redirect_url=redirect_url):
                self.assertRedirects(user.get(url), redirect_url)
