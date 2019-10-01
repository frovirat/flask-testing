"""
Schemas used in text processing
"""
from flask_restplus import Model, fields

stats_texts_schema = Model(
    'Text_processed', {
        'text_processed_stat': fields.Integer(required=True, description='Number of text processed')
    }
)

stats_words_schema = Model(
    'Words_found_stat', {
        'words_found': fields.Integer(required=True, description='Number of words found')
    }
)

stats_chars_schema = Model(
    'Chars_found_stat', {
        'characters_found': fields.Integer(required=True, description='Number of chars found')
    }
)

stats_schema = Model(
    'Stats', {
        'text_processed_stat': fields.Integer(
            required=True, description='Number of texts processed'),
        'words_found': fields.Integer(required=True, description='Number of words found'),
        'characters_found': fields.Integer(required=True, description='Number of characters found')
    }
)

count_schema = Model(
    'CountedText', {
        'words': fields.Integer(required=True, description='Number words found'),
        'characters': fields.Integer(required=True, description='Number of characters found')
    }
)
