from motor import motor_asyncio
from config import load_config

config = load_config()


class MongoDB:
    client = None
    db = None

    @staticmethod
    def get_client():
        if MongoDB.client is None:
            # MONGODB_USERNAME = config.db.username
            # MONGODB_PASSWORD = config.db.password
            MONGODB_HOSTNAME = config.db.host
            MONGODB_PORT = config.db.port

            # MongoDB.client = motor_asyncio.AsyncIOMotorClient("mongodb://{}:{}@{}:{}".format(
            #     MONGODB_USERNAME, MONGODB_PASSWORD, MONGODB_HOSTNAME, str(MONGODB_PORT)))
            MongoDB.client = motor_asyncio.AsyncIOMotorClient("mongodb://{}:{}".format(
                MONGODB_HOSTNAME, str(MONGODB_PORT)))

        return MongoDB.client

    @staticmethod
    def get_data_base():
        if MongoDB.db is None:
            client = MongoDB.get_client()
            MongoDB.db = client[config.db.database]

        return MongoDB.db

    @staticmethod
    async def add_group(group_name: str, group_id: str):
        await MongoDB.get_data_base().groups.update_one(
            filter={'group_id': group_id},
            update={"$set": {"group_name": group_name}},
            upsert=True,
        )

    @staticmethod
    async def get_groups():
        async for group in MongoDB.get_data_base().groups.find():
            yield group

    @staticmethod
    async def set_post(group_id: str, message_id: str, chat_id: str):
        await MongoDB.get_data_base().groups.update_one(
            filter={'group_id': group_id},
            update={"$set": {"message_id": message_id, "chat_id": chat_id}},
            upsert=True,
        )

    @staticmethod
    async def get_post(group_id: str):
        post = await MongoDB.get_data_base().groups.find_one({'group_id': group_id})
        return post

    @staticmethod
    async def update_post(group_id: str, data: dict):
        await MongoDB.get_data_base().groups.update_one(
            filter={'group_id': group_id},
            update={"$set": data},
            upsert=True,
        )
