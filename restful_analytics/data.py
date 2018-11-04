from uuid import uuid4
from flask_restplus import Resource, reqparse

class _DataResource(Resource):
    _data_dict = {}

    @classmethod
    def data_dict(cls):
        return cls._data_dict

    def _representation(self, id):
        return {
                'href': self.api.url_for(DataInstance, id=id, _external=True),
                'type': type(_DataResource._data_dict[id]).__name__,
                'value': _DataResource._data_dict[id],
        }

class DataCollection(_DataResource):
    @classmethod
    def reset(cls):
        cls._data_dict = {}

    def get(self):
        return {
                'href': self.api.url_for(self.__class__, _external=True),
                'collection': [self._representation(id) for id in _DataResource._data_dict.keys()],
        }

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('python')
        id = str(uuid4())
        _DataResource._data_dict[id] = eval(parser.parse_args()['python'])
        return self._representation(id), 201, {'Location': self.api.url_for(DataInstance, id=id)}

class DataInstance(_DataResource):
    def get(self, id):
        try:
            return self._representation(id)
        except KeyError:
            return {'errors': ['No such datum']}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('python')
        _DataResource._data_dict[id] = eval(parser.parse_args()['python'])
        return _DataResource._data_dict[id]

    def delete(self, id):
        try:
            del _DataResource._data_dict[id]
        except KeyError:
            return {'errors': ['No such datum']}, 404
