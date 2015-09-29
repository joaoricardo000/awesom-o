from pymongo import MongoClient


class ServiceLocator:
    def __init__(self):
        self.connection = None
        self.collection = None
        self.web_layer = None

    def set_web_layer(self, web_layer):
        self.web_layer = web_layer

    def get_db_collection(self):
        if not self.collection:
            self.connection = MongoClient('localhost', 27017)
            self.collection = self.connection.whatsapp
        return self.collection


Instance = ServiceLocator()
