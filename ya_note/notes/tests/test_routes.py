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
    REDIRECT_URL
)


class TestRoutes(TestBaseClass):

    def test_availability_for_pages(self):
        parametrized_options = (
            (DETAIL_SLUG_URL, self.auth_author, HTTPStatus.OK),
            (DETAIL_SLUG_URL, self.auth_other_user, HTTPStatus.NOT_FOUND),
            (EDIT_SLUG_URL, self.auth_author, HTTPStatus.OK),
            (EDIT_SLUG_URL, self.auth_other_user, HTTPStatus.NOT_FOUND),
            (DELETE_SLUG_URL, self.auth_author, HTTPStatus.OK),
            (DELETE_SLUG_URL, self.auth_other_user, HTTPStatus.NOT_FOUND),
            (NOTES_LIST_URL, self.auth_author, HTTPStatus.OK),
            (NOTES_ADD_URL, self.auth_author, HTTPStatus.OK),
            (NOTES_SUCCESS_URL, self.auth_author, HTTPStatus.OK),
            (NOTES_HOME_URL, self.client, HTTPStatus.OK),
            (LOGIN_URL, self.client, HTTPStatus.OK),
            (LOGOUT_URL, self.client, HTTPStatus.OK),
            (SIGN_UP_URL, self.client, HTTPStatus.OK),
        )
        for url, user, status in parametrized_options:
            with self.subTest(url=url, user=user, status=status):
                if url == LOGOUT_URL:
                    self.assertEqual(user.post(url).status_code, status)
                else:
                    self.assertEqual(user.get(url).status_code, status)

    def test_redirect_for_anonymous_client(self):
        parametrized_options = (
            (EDIT_SLUG_URL, self.client),
            (DELETE_SLUG_URL, self.client),
            (DETAIL_SLUG_URL, self.client),
            (NOTES_LIST_URL, self.client),
            (NOTES_ADD_URL, self.client),
            (NOTES_SUCCESS_URL, self.client)
        )
        for url, user in parametrized_options:
            with self.subTest(url=url, user=user):
                self.assertRedirects(user.get(url), REDIRECT_URL + url)
