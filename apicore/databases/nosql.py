from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from ..exceptions import Http400Exception, Http404Exception, Http409Exception

# TODO host, port, ssl, login, password from config file
client = MongoClient(connect=False)


class Db:
    db = client["wiri"]  # TODO from config file

    @classmethod
    def getMany(cls, collection, offset=0, limit=0, sort=None):
        return list(cls.db[collection].find({}, skip=offset, limit=limit, sort=sort))

    @classmethod
    def get(cls, collection, identifier, key="_id"):
        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        data = cls.db[collection].find_one({key: identifier})
        if data:
            return data
        else:
            raise Http404Exception()

    @classmethod
    def post(cls, data, collection):
        try:
            return cls.db[collection].insert_one(data).inserted_id
        except errors.DuplicateKeyError:
            raise Http409Exception("Already registered")

    @classmethod
    def patch(cls, data, collection, identifier, key="_id"):
        if key == "_id":
            try:
                value = ObjectId(identifier)
            except:
                raise Http400Exception()

        cls.db[collection].update_one({key: value}, {'$set': data})

    @classmethod
    def patchMany(cls, data, collection, identifier, key="_id"):
        if key == "_id":
            try:
                value = ObjectId(identifier)
            except:
                raise Http400Exception()

        cls.db[collection].update_many({key: value}, {'$set': data})

    @classmethod
    def put(cls, data, collection, identifier, key="_id"):
        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        resu = cls.db[collection].replace_one({key: identifier}, data, True)

    @classmethod
    def delete(cls, collection, identifier, key="_id"):
        if key == "_id":
            try:
                identifier = ObjectId(identifier)
            except:
                raise Http400Exception()

        cls.db[collection].delete_one({key: identifier})
