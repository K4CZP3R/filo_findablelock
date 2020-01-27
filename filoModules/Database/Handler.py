import pymongo, config

from filoModules.Debug import Debug
from filoModules import Models


class Handler:  # method/constructor overloading: a
    def __init__(self, collection_name):
        self.client = pymongo.MongoClient(config.get_mongo_config().get_url())
        self.collection_name = collection_name
        self.collection = self.client['filo'][collection_name]
        self.debug = Debug(
            f"DbHandler({collection_name})", enabled=False
        )

    def find_all(self):
        self.debug.print_v(f"Finding it all! col:{self.collection_name}")
        return self.collection.find({})

    def drop_all(self):
        self.debug.print_w(f"Dropping whole database!")
        return self.client.drop_database('filo')

    def drop_col(self):
        self.debug.print_w(f"Dropping col:{self.collection_name}")
        return self.collection.drop()

    def find_one(self, search_dict: dict):
        self.debug.print_v(
            f"Searching for dict ({search_dict}) in '{self.collection_name}'")
        return self.collection.find_one(search_dict)

    def insert_one(self, insert_dict: dict):
        self.debug.print_v(
            f"Inserting dict ({insert_dict}) in '{self.collection_name}'")
        return self.collection.insert_one(insert_dict)

    def update_one(self, query: dict, new_values: dict):
        self.debug.print_v(
            f"Updating dict ({query}) with '{new_values}' in '{self.collection_name}'")
        return self.collection.update_one(query, new_values)

    def delete_one(self, delete_dict: dict):
        self.debug.print_v(
            f"Deleting dict ({delete_dict}) in '{self.collection_name}'")
        return self.collection.delete_one(delete_dict)
