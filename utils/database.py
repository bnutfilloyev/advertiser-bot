from motor import motor_asyncio
from config import load_config

config = load_config()


class MongoDB:
    client = None
    db = None

    @staticmethod
    def get_client():
        if MongoDB.client is None:
            # MongoDB.client = motor_asyncio.AsyncIOMotorClient("mongodb://{}:{}@{}:{}".format(
            #     config.db.username, config.db.password, config.db.host, config.db.port))

            MongoDB.client = motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
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
    async def remove_group(group_id: str):
        await MongoDB.get_data_base().groups.delete_one({'group_id': group_id})

    @staticmethod
    async def get_groups():
        async for group in MongoDB.get_data_base().groups.find():
            yield group

    @staticmethod
    async def set_post(group_id: str, message_id: str, chat_id: str):
        req = await MongoDB.get_data_base().posts.insert_one(
            {"group_id": group_id, "message_id": message_id, "chat_id": chat_id}
        )
        return req.inserted_id

    @staticmethod
    async def update_groups(group_id: str, data: dict):
        await MongoDB.get_data_base().groups.update_one(
            filter={'group_id': group_id},
            update={"$set": data},
            upsert=True,
        )

    @staticmethod
    async def get_post(group_id: str):
        return await MongoDB.get_data_base().groups.find_one({"group_id": group_id})

    @staticmethod
    async def remove_posts(group_id: str):
        async for post in MongoDB.get_data_base().posts.find({"group_id": group_id}):
            await MongoDB.get_data_base().posts.delete_one({"_id": post.get('_id')})

    @staticmethod
    async def get_all_posts(group_id: str):
        async for post in MongoDB.get_data_base().posts.find({"group_id": group_id}):
            yield post
