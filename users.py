from pymongo import MongoClient

import os

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)

# Connect to the test db
db = client.tbot


class User:

    # def __init__(self):
    #     self.access = False

    def add(self, data):
        user = db.users
        user_details = {
            'Name': data['Name'],
            '_id': data['ID'],
            'access': data['access'],
            'reg_date': data['reg_date'],
            'sub_start_date': data['sub_start_date'],
            'sub_end_date': data['sub_end_date']
        }

        Queryresult = user.find_one({'_id': data['ID']})

        if Queryresult is None:
            result = user.insert_one(user_details)
            print('Добавлен юзер')
        else:
            print('Юзер уже есть')

    def getUserByID(self, ID):
        print('Поиск юзера')
