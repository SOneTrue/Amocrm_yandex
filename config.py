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
class DbConfig:
    user_db: str
    password_db: str
    address_db: str
    port_db: str
    name_db: str


@dataclass
class Config:
    reports: Reports
    yandex_token: YandexToken
    yandex_login: YandexLogin
    db: DbConfig


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
        db=DbConfig(
            user_db=env.str('USER_DB'),
            password_db=env.str('PASSWORD_DB'),
            address_db=env.str('ADDRESS_DB'),
            port_db=env.str('PORT_DB'),
            name_db=env.str('NAME_DB')

        ),
    )
