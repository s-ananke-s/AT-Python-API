from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Get user")
class TestUserGet(BaseCase):
    @allure.title("Поулчение данных пользователя неавторизованным пользователем")
    def test_get_user_details_not_auth(self):
        with allure.step("Пытаемся получить данные пользователя с id 2"):
            response = MyRequests.get("/user/2")
        with allure.step("Проверяем, что доступен username"):
            Assertions.assert_json_has_key(response, "username")
        with allure.step("Проверяем, что не доступен email"):
            Assertions.assert_json_has_not_key(response, "email")
        with allure.step("Проверяем, что не доступен firstName"):
            Assertions.assert_json_has_not_key(response, "firstName")
        with allure.step("Проверяем, что не доступен lastName"):
            Assertions.assert_json_has_not_key(response, "lastName")

    @allure.title("Получение данных пользователя авторизованным пользователем")
    def test_get_user_details_auth_as_same_user(self):
        with allure.step("Заходим под пользователем с id 2"):
            data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
            response1 = MyRequests.post("/user/login", data=data)
        with allure.step("Запоминаем данные этого пользователя"):
            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")
        with allure.step("Пытаемся получить данные пользователя с id 2"):
            response2 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                       headers = {"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        with allure.step("Проверяем, что все поля доступны"):
            expected_fields = ["username", "email", "firstName", "lastName"]
            Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.title("Получение данных пользователя другим авторизованным пользователем")
    def test_get_other_user(self):
        with allure.step("Заходим под пользователем с id 2"):
            data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }
            response1 = MyRequests.post("/user/login", data=data)
        with allure.step("Запоминаем данные этого пользователя"):
            auth_sid = self.get_cookie(response1, "auth_sid")
            token = self.get_header(response1, "x-csrf-token")
            user_id_from_auth_method = self.get_json_value(response1, "user_id")
            print(user_id_from_auth_method)
        with allure.step("Пытаемся получить данные другого пользователя с id 1"):
            response2 = MyRequests.get("/user/1", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        with allure.step("Проверяем, что доступен username"):
            Assertions.assert_json_has_key(response2, "username")
        with allure.step("Проверяем, что не доступен email"):
            Assertions.assert_json_has_not_key(response2, "email")
        with allure.step("Проверяем, что не доступен firstName"):
            Assertions.assert_json_has_not_key(response2, "firstName")
        with allure.step("Проверяем, что не доступен lastName"):
            Assertions.assert_json_has_not_key(response2, "lastName")
