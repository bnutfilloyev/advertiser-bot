from environs import Env
from pydantic import BaseModel


class Bot(BaseModel):
    """
    Bot configuration
    """
    token: str
    admins: list


class Database(BaseModel):
    """
    Database configuration
    """
    host: str
    port: int
    user: str = None
    password: str = None
    database: str


class Config(BaseModel):
    """
    Configuration model
    """
    bot: Bot
    db: Database = None


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        bot=Bot(
            token=env.str("BOT_TOKEN"),
            admins=env.list("ADMINS"),
        ),
        db=Database(
            host=env.str("DB_HOST"),
            port=env.int("DB_PORT"),
            # user=env.str("DB_USER"),
            # password=env.str("DB_PASSWORD"),
            database=env.str("DB_DATABASE"),
        ),
    )


if __name__ == "__main__":
    config = load_config()
    print(config)
    print(config.bot.token)
    print(config.bot.admins)
    # print(ADMINS)
    # print(USE_MONGODB)
    # print(MONGODB_USERNAME)
    # print(MONGODB_PASSWORD)
    # print(MONGODB_HOSTNAME)
    # print(MONGODB_PORT)
