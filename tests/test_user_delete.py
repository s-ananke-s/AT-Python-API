from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import time


class TestUserDelete(BaseCase):
    def test_delete_user_with_id_2(self):
        # Login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Delete
        response2 = MyRequests.delete(f"/user/2",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid},
                                     )
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5."

    def test_delete_authorized_user(self):
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

        # Delete
        response2 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid},
                                      )
        Assertions.assert_code_status(response2, 200)


        #Get
        time.sleep(1)
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})
        assert response4.content.decode("utf-8") == f"User not found"

    def test_delete_another_user(self):
        # Register first
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']

        # Register second
        time.sleep(1)
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

        # Delete second user

        response4 = MyRequests.delete(f"/user/{user_id2}",
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
        assert response6.content.decode("utf-8") != f"User not found"
