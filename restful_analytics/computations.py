from uuid import uuid4
from flask_restplus import Resource, reqparse
from .data import DataCollection, DataInstance
from .providers import AnalyticInstance, load_function
import numpy

class _ComputationResource(Resource):
    _computation_dict = {}

class ComputationCollection(_ComputationResource):
    @classmethod
    def reset(cls):
        cls._computation_dict = {}

    def get(self):
        return {
                'href': self.api.url_for(self.__class__, _external=True),
                'collection': list(_ComputationResource._computation_dict),
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('provider', type=str, required=True)
        parser.add_argument('analytic', type=str, required=True)
        parser.add_argument('operand', action='append', required=True)
        args = parser.parse_args()
        module_name = args['provider']
        function_name = args['analytic']
        function = load_function(module_name, function_name)
        operand_list = args['operand']
        operands = []
        for operand in operand_list:
            if operand.startswith(self.api.base_url):
                last_slash = operand.rindex('/')
                datum_id = operand[last_slash + 1:]
                operands.append(DataCollection.data_dict()[datum_id])
            else:
                operands.append(eval(operand))
        id = str(uuid4())
        result = function(*operands)
        DataCollection.data_dict()[id] = self._xlate_numpy(result)
        _ComputationResource._computation_dict[id] = {
                'href': self.api.url_for(ComputationInstance, id=id, _external=True),
                'operation': self.api.url_for(AnalyticInstance, provider=module_name, analytic=function_name, _external=True),
                'operands': args['operand'],
                'result': self.api.url_for(DataInstance, id=id, _external=True),
        }
        return (_ComputationResource._computation_dict[id], 201,
                {'Location': self.api.url_for(ComputationInstance, id=id, _external=True)})

    def _xlate_numpy(self, obj):
        '''This hack keeps numpy types out of data_dict until I can get custom JSON encoders to work.'''
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return obj

class ComputationInstance(_ComputationResource):
    def get(self, id):
        try:
            return _ComputationResource._computation_dict[id]
        except KeyError:
            return {'errors': ['No such computation']}, 404

    def delete(self, id):
        try:
            del _ComputationResource._computation_dict[id]
        except KeyError:
            return {'errors': ['No such computation']}, 404
