from environs import Env
from pydantic import BaseModel


class DbConfig(BaseModel):
    host: str
    password: str
    user: str
    database: str


class TgBot(BaseModel):
    token: str
    admin_ids: list[int]
    use_redis: bool


class Miscellaneous(BaseModel):
    other_params: str = None


class Config(BaseModel):
    bot: TgBot
    database: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        database=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous()
    )
