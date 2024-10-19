from os import getenv
from typing import Union

import certifi
from pymongo.mongo_client import MongoClient

Uri = getenv("MONGODB_URI")
Client = MongoClient(Uri, tlsCAFILE=certifi.where())["Discord_Splitter"]


class Guild:

    # ----- /// Criar e deletar /// ----- #
    @staticmethod
    def create_document(Discord_ID: str) -> None:

        if Client["Server_Info"].find_one({"Discord_ID": Discord_ID}) is None:
            Client["Server_Info"].insert_one(
                {
                    "Discord_ID": Discord_ID,
                    "Topics": [],
                    "Users_Per_Room": 2,
                    "Time": 5,
                }
            )

    @staticmethod
    def change_Topic(Discord_ID: str, Topics: list) -> Union[None, int]:
        result = Client["Server_Info"].find_one({"Discord_ID": Discord_ID})

        if not result:
            return -1

        else:
            Client["Server_Info"].update_one(
                {"Discord_ID": Discord_ID}, {"$set": {"Topics": Topics}}
            )
            return 0

    @staticmethod
    def change_UPR(Discord_ID: str, UPR: int) -> Union[None, int]:
        result = Client["Server_Info"].find_one({"Discord_ID": Discord_ID})

        if not result:
            return -1

        else:
            Client["Server_Info"].update_one(
                {"Discord_ID": Discord_ID}, {"$set": {"Users_Per_Room": UPR}}
            )
            return 0

    @staticmethod
    def change_time(Discord_ID: str, time: int) -> int:
        Client["Server_Info"].update_one(
            {"Discord_ID": Discord_ID}, {"$set": {"Time": time}}
        )
        return 0

    @staticmethod
    def reset_topics(Discord_ID: str) -> int:
        result = Client["Server_Info"].update_one(
            {"Discord_ID": Discord_ID}, {"$set": {"Topics": []}}
        )

        if result.matched_count == 0:
            return -1
        if result.modified_count == 1:
            return 0

        return "No changes made"

    @staticmethod
    def delete_document(Discord_ID: str) -> Union[None, str]:
        result = Client["Server_Info"].find_one({"Discord_ID": Discord_ID})

        if not result:
            return "Server Not Found"
        else:
            Client["Server_Info"].delete_one({"Discord_ID": Discord_ID})

    # ----- /// Pegar valores // ----- #

    @staticmethod
    def get_topics(Discord_ID: str) -> list:
        result = Client["Server_Info"].find_one({"Discord_ID": Discord_ID})

        if not result:
            return "Server Not Found"
        else:
            return result.get("Topics")

    @staticmethod
    def get_UPR(Discord_ID: str) -> int:
        result = Client["Server_Info"].find_one({"Discord_ID": Discord_ID})

        return result.get("Users_Per_Room")

    @staticmethod
    def get_time(Discord_ID: str) -> int:
        result = Client["Server_Info"].find_one({"Discord_ID": Discord_ID})
        return int(result.get("Time"))
