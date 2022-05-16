from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import pytest
import allure


@allure.epic("Register user")
class TestUserRegister(BaseCase):
    user_data = [
        ("", "learqa", "learqa", "learqa", "leanqatest1@example.com"),
        ("123", "", "learqa", "learqa", "leanqatest2@example.com"),
        ("123", "learqa", "", "learqa", "leanqatest3@example.com"),
        ("123", "learqa", "learqa", "", "leanqatest4@example.com"),
        ("123", "learqa", "learqa", "learqa", "")
    ]
    tags = ("password", "username", "firstname", "lastname", "email")

    @allure.severity("blocker")
    @allure.title("Успешное создание пользователя")
    def test_create_user_successfully(self):
        with allure.step("Генерируем корректные данные для регистрации"):
            data = self.prepare_registration_data()
            response = MyRequests.post("/user/", data=data)
        with allure.step("Проверяем что id возвращается в ответе - пользователь создался"):
            Assertions.assert_code_status(response, 200)
            Assertions.assert_json_has_key(response, "id")

    @allure.severity("blocker")
    @allure.title("Создание пользователя с существующим email")
    def test_create_user_with_existing_email(self):
        with allure.step("Генерируем существующий email"):
            email = 'vinkotov@example.com'
            data = self.prepare_registration_data(None,email)
            response = MyRequests.post("/user/", data=data)
        with allure.step("Проверяем что email некоррекный"):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.severity("blocker")
    @allure.title("Создание пользователя с некорректным email")
    def test_create_user_with_incorrect_email(self):
        with allure.step("Генерируем некорректный email"):
            random_string = self.generate_random_string(5)
            email = f'test-example{random_string}.com'
            data = self.prepare_registration_data(None,email)
            response = MyRequests.post("/user/", data=data)
        with allure.step("Проверяем что email некоррекный"):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"Invalid email format"

    @allure.feature("Проверки на некоррекное имя")
    @allure.severity("critical")
    @allure.title("Создание пользователя с очень коротким именем")
    def test_create_user_with_short_name(self):
        with allure.step("Генерируем username с очень маленьким количеством символов"):
            username = 'a'
            data = self.prepare_registration_data(username, None)
            response = MyRequests.post("/user/", data=data)
        with allure.step("Проверяем что username некоррекный"):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The value of 'username' field is too short"

    @allure.feature("Проверки на некоррекное имя")
    @allure.severity("critical")
    @allure.title("Создание пользователя с очень длинным именем")
    def test_crete_user_with_long_name(self):
        with allure.step("Генерируем username с очень большим количеством символов"):
            username = self.generate_random_string(251)
            data = self.prepare_registration_data(username, None)
            response = MyRequests.post("/user/", data=data)
        with allure.step("Проверяем что username некоррекный"):
            Assertions.assert_code_status(response, 400)
            assert response.content.decode("utf-8") == f"The value of 'username' field is too long"

    @allure.story("Обязательность полей")
    @allure.severity("blocker")
    @allure.title("Проверка обязательности всех полей при регистрации {tags}")
    @pytest.mark.parametrize("password,username,firstname,lastname,email", user_data)
    def test_create_user_without_any_field(self, password, username, firstname, lastname, email):
        with allure.step("Заполняем данные с отсутствуеющим одним полем"):
            data = {'password': password, 'username': username, 'firstName': firstname, 'lastName': lastname,
                    'email': email}
            response = MyRequests.post("/user/", data=data)
            Assertions.assert_code_status(response, 400)
        with allure.step("Проверка обязательности полей"):
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
