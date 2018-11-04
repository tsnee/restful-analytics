from flask import Flask
from flask_restplus import Api
from . import computations
from . import data
from . import encoder
from . import providers

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)
    app.json_encoder = encoder.StrEncoder   # This seems to have no effect.
    create_api(app)
    return app

def create_api(app):
    api = Api(app)

    computations.ComputationCollection.reset()
    data.DataCollection.reset()

    api.add_resource(providers.ProviderCollection, '/providers')
    api.add_resource(providers.ProviderInstance, '/providers/<string:provider>')
    api.add_resource(providers.AnalyticInstance, '/providers/<string:provider>/<string:analytic>')
    api.add_resource(providers.DocumentationInstance, '/documentation/<string:provider>',
            '/documentation/<string:provider>/<string:analytic>')
    api.add_resource(data.DataCollection, '/data')
    api.add_resource(data.DataInstance, '/data/<string:id>')
    api.add_resource(computations.ComputationCollection, '/computations')
    api.add_resource(computations.ComputationInstance, '/computations/<string:id>')
    return api
