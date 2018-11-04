import inspect
import sys
import pydoc
from importlib import import_module
from flask import Response
from flask_restplus import Resource

def load_module(module_name):
    if module_name in sys.modules:
        return sys.modules[module_name]
    else:
        return import_module(module_name)

def load_function(module_name, function_name):
    module = load_module(module_name)
    return getattr(module, function_name)

class ProviderCollection(Resource):
    def get(self):
        return {
                'href': self.api.url_for(self.__class__, _external=True),
                'collection': [
                    {
                        'href': self.api.url_for(ProviderInstance, provider='numpy', _external=True),
                        'name': 'numpy',
                        'documentation': self.api.url_for(DocumentationInstance, provider='numpy', _external=True),
                    },
                ]
        }

class ProviderInstance(Resource):
    def get(self, provider):
        try:
            module = load_module(provider)
            analytic_list = inspect.getmembers(module, lambda f: inspect.isfunction(f))
            return {
                    'href': self.api.url_for(self, provider=provider, _external=True),
                    'name': provider,
                    'documentation': self.api.url_for(DocumentationInstance, provider=provider, _external=True),
                    'analytics': [{'name': analytic[0],
                                   'href': self.api.url_for(AnalyticInstance, provider=provider,
                                       analytic=analytic[0], _external=True),
                                   'documentation': self.api.url_for(DocumentationInstance, provider=provider,
                                       analytic=analytic[0], _external=True),
                                  } for analytic in analytic_list],
            }
        except ModuleNotFoundError:
            return {'errors': ['No such provider']}, 404

class AnalyticInstance(Resource):
    def get(self, provider, analytic):
        try:
            function = load_function(provider, analytic)
            return {
                    'name': analytic,
                    'href': self.api.url_for(self, provider=provider, analytic=analytic, _external=True),
                    'documentation': self.api.url_for(DocumentationInstance, provider=provider,
                        analytic=analytic, _external=True),
                    'signature': str(inspect.signature(function)),
            }
        except ModuleNotFoundError:
            return {'errors': ['No such provider']}, 404
        except AttributeError:
            return {'errors': ['No such anlytic in provider']}, 404

class DocumentationInstance(Resource):
    def get(self, provider, analytic=None):
        obj = load_module(provider)
        if analytic != None:
            obj = getattr(obj, analytic)
        html = pydoc.html.document(obj)
        return Response(response=html, mimetype='text/html')
