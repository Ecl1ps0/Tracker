import requests

from configs.logger import get_logger

logger = get_logger(__name__)


class Login:
    def __init__(self):
        self.is_logged_in = False
        self.__login_url = "http://localhost:8080/auth/signin"
        self.token = None

    def __login(self, login: str, password: str) -> str | None:
        json_data = {
            "Email": login,
            "Password": password
        }

        response = requests.post(url=self.__login_url, json=json_data)
        if response:
            self.is_logged_in = True
            return response.json()["token"]

        return None

    def start_login(self) -> None:
        while not self.is_logged_in:
            email = input("Please write your email: ")
            password = input("Please write your password: ")
            self.token = self.__login(email, password)
            logger.info(f"Token is {self.token}")
            print(self.token)

            if not self.is_logged_in:
                logger.info("Wrong email or password!")
                print("Wrong email or password, please try again!")
