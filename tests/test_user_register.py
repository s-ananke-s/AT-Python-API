from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest


class TestUserRegister(BaseCase):

    user_data = [
        ("","learqa","learqa","learqa","leanqatest1@example.com"),
        ("123","","learqa","learqa","leanqatest2@example.com"),
        ("123","learqa","","learqa","leanqatest3@example.com"),
        ("123","learqa","learqa","","leanqatest4@example.com"),
        ("123","learqa","learqa","learqa","")
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_create_user_with_incorrect_email(self):
        email = 'test-example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

    def test_create_user_with_short_name(self):
        username = 'a'
        data = self.prepare_registration_data(username)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'email' field is too short"

    def test_crete_user_with_long_name(self):
        username = self.generate_random_string(251)
        data = self.prepare_registration_data(username)
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'email' field is too long"

    @pytest.mark.parametrize("password,username,firstname,lastname,email", user_data)
    def test_create_user_without_any_field(self, password, username, firstname, lastname, email):
        data = {'password': password, 'username': username, 'firstName': firstname, 'lastName': lastname,
                'email': email}
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        if password == "":
            assert response.content.decode("utf-8") == f"The value of 'password' field is too short"
        elif username == "":
            assert response.content.decode("utf-8") == f"The value of 'username' field is too short"
        elif firstname == "":
            assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short"
        elif lastname == "":
            assert response.content.decode("utf-8") == f"The value of 'lastName' field is too short"
        elif email == "":
            assert response.content.decode("utf-8") == f"The value of 'email' field is too short"
