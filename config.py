from dataclasses import dataclass

from environs import Env


@dataclass
class Reports:
    reports_url: str
    token_type: str


@dataclass
class YandexToken:
    token_one: str
    token_two: str
    token_three: str


@dataclass
class YandexLogin:
    login_one: str
    login_two: str
    login_three: str


@dataclass
class Config:
    reports: Reports
    yandex_token: YandexToken
    yandex_login: YandexLogin


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        reports=Reports(
            reports_url=env.str("REPORTS_URL"),
            token_type=env.str("TOKEN_TYPE"),
        ),
        yandex_token=YandexToken(
            token_one=env.str("TOKEN_ONE"),
            token_two=env.str("TOKEN_TWO"),
            token_three=env.str("TOKEN_THREE"),
        ),
        yandex_login=YandexLogin(
            login_one=env.str("LOGIN_ONE"),
            login_two=env.str("LOGIN_TWO"),
            login_three=env.str("LOGIN_THREE"),
        ),
    )
    #     db=DbConfig(
    #         host=env.str('DB_HOST'),
    #         password=env.str('DB_PASS'),
    #         user=env.str('DB_USER'),
    #         database=env.str('DB_NAME')
    #     ),
    #     misc=Miscellaneous()
    # )
