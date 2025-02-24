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
        options = (
            (
                DETAIL_SLUG_URL,
                self.auth_author.get,
                HTTPStatus.OK
            ),
            (
                DETAIL_SLUG_URL,
                self.auth_other_user.get,
                HTTPStatus.NOT_FOUND
            ),
            (
                EDIT_SLUG_URL,
                self.auth_author.get,
                HTTPStatus.OK
            ),
            (
                EDIT_SLUG_URL,
                self.auth_other_user.get,
                HTTPStatus.NOT_FOUND
            ),
            (
                EDIT_SLUG_URL,
                self.client.get,
                HTTPStatus.FOUND,
                REDIRECT_EDIT_SLUG_URL
            ),
            (
                DELETE_SLUG_URL,
                self.auth_author.get,
                HTTPStatus.OK
            ),
            (
                DELETE_SLUG_URL,
                self.auth_other_user.get,
                HTTPStatus.NOT_FOUND
            ),
            (
                DELETE_SLUG_URL,
                self.client.get,
                HTTPStatus.FOUND,
                REDIRECT_DELETE_SLUG_URL
            ),
            (
                NOTES_LIST_URL,
                self.auth_author.get,
                HTTPStatus.OK
            ),
            (
                NOTES_ADD_URL,
                self.auth_author.get,
                HTTPStatus.OK
            ),
            (
                NOTES_SUCCESS_URL,
                self.auth_author.get,
                HTTPStatus.OK
            ),
            (
                NOTES_HOME_URL,
                self.client.get,
                HTTPStatus.OK
            ),
            (
                LOGIN_URL,
                self.client.get,
                HTTPStatus.OK
            ),
            (
                LOGOUT_URL,
                self.client.post,
                HTTPStatus.OK
            ),
            (
                SIGN_UP_URL,
                self.client.get,
                HTTPStatus.OK
            ),
        )
        for url, client_method, expected_status, *expected_redirect in options:
            redirect = expected_redirect[0] if expected_redirect else None
            with self.subTest(
                url=url,
                client_method=client_method,
                expected_status=expected_status,
            ):
                assert (
                    client_method(url).status_code == expected_status
                    and (not expected_status == HTTPStatus.FOUND
                         or client_method(url).headers['Location'] == redirect)
                )
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
