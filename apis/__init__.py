"""
Api generationan including all the namespaces
"""
from flask_restplus import Api

from apis.text_processing import api as text_processing_api

api = Api(
    title='EDD oct 2019',
    version='1.0',
    description='Api for EDD oct 2019',
)

api.add_namespace(text_processing_api)
