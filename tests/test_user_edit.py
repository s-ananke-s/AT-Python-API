from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import json

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        #Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        #Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #Edit
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                 )
        Assertions.assert_code_status(response3, 200)

        #Get
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers = {"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name of user after edit")

    def test_user_edit_not_authorized(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # Edit
        new_name = "Changed name"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   data={"firstName": new_name}
                                   )
        Assertions.assert_code_status(response3, 400)
        print(response3.content)

    def test_user_edit_another_user_authorized(self):
        # Register first
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']

        # Register second
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data2['email']
        first_name2 = register_data2['firstName']
        password2 = register_data2['password']
        user_id2 = self.get_json_value(response2, "id")

        # Login first user
        login_data = {
            'email': email,
            'password': password
        }
        response3 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")
        print(response3.content)

        # Edit second user

        new_name = "Changed name"
        response4 = MyRequests.put(f"/user/{user_id2}",
                                   data={"firstName": new_name},
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        print(response4.content)

        # Login second user

        login_data = {
            'email': email2,
            'password': password2
        }
        response5 = MyRequests.post("/user/login", data=login_data)

        auth_sid2 = self.get_cookie(response5, "auth_sid")
        token2 = self.get_header(response5, "x-csrf-token")
        print(response5.content)

        # Get second user

        response6 = MyRequests.get(f"/user/{user_id2}",
                                   headers={"x-csrf-token": token2},
                                   cookies={"auth_sid": auth_sid2})
        Assertions.assert_json_value_by_name(response6, "firstName", first_name2, "Wrong name of user after edit")

    def test_edit_email_to_wrong_by_authorized_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Change email
        new_email = "test-example.com"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email}
                                   )
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == f"Invalid email format"

    def test_edit_first_name_to_short_by_authorized_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Change first name
        new_firstname = "n"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_firstname}
                                   )
        Assertions.assert_code_status(response3, 400)
        error_to_dict = response3.content.decode("utf-8")
        obj = json.loads(error_to_dict)
        error = obj["error"]
        assert error == "Too short value for field firstName"
