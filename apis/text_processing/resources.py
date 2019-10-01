"""
Text processing count resources
"""
from flask_restplus import Namespace, Resource, marshal_with

from .controllers import TextProcessingController
from .schemas import (count_schema, stats_chars_schema, stats_schema,
                      stats_texts_schema, stats_words_schema)

api = Namespace('text_processing', description='text processing operations')

api.models[stats_texts_schema.name] = stats_texts_schema
api.models[count_schema.name] = count_schema
api.models[stats_chars_schema.name] = stats_chars_schema
api.models[stats_words_schema.name] = stats_words_schema
api.models[stats_schema.name] = stats_schema


@api.route('/')
@api.doc('Return stats about processing activity since the service is online')
class TextProcessingResource(Resource):
    """
    Text processing resource for base route
    """
    @api.marshal_with(stats_texts_schema)
    @api.response(200, 'Success', stats_texts_schema)
    def get(self):
        """ Implementation of get method """
        return TextProcessingController.get_stats()

    @api.response(200, 'Success')
    def delete(self):
        """ Implementation of delete method """
        return TextProcessingController.reset_stats()


@api.route('/count')
@api.doc('Count the elements in a given text')
class TextProcessingCount(Resource):
    """
    Text processing resource for /count route
    """
    parser = api.parser()
    parser.add_argument('text', type=str, location='form', default='')
    @api.expect(parser, validate=True)
    @marshal_with(count_schema)
    @api.response(200, 'Success', count_schema)
    def post(self):
        """ Implementation of post method """
        text = self.parser.parse_args().get('text', '')
        return TextProcessingController.count_elements(text)

    @marshal_with(stats_schema)
    @api.response(200, 'Success', stats_schema)
    def get(self):
        """ Implementation of get method """
        return TextProcessingController.get_stats()

@api.route('/count/word')
@api.doc('Count the words in a given text')
class TextProcessingCountWord(Resource):
    """
    Text processing resource for /count/word route
    """
    parser = api.parser()
    parser.add_argument('text', type=str, location='form', default='')
    parser.add_argument('words', action='append', default=[])
    @api.expect(parser, validate=True)
    @marshal_with(stats_words_schema)
    @api.response(200, 'Success', stats_words_schema)
    def post(self):
        """ Implementation of post method """
        text = self.parser.parse_args().get('text', '')
        words = self.parser.parse_args().get('words', [])
        return TextProcessingController.count_words(text, words)
