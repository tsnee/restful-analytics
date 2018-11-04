from flask.json import JSONEncoder
import numpy

class StrEncoder(JSONEncoder):
    def default(self, obj):
        print('obj: {}'.format(obj))
        try:
            return super(JSONEncoder, self).default(obj)
        except TypeError:
            print('falling back on str()')
            if isinstance(obj, numpy.integer):
                return int(obj)
            elif isinstance(obj, numpy.floating):
                return float(obj)
            elif isinstance(obj, numpy.ndarray):
                return obj.tolist()
            else:
                return str(obj)
