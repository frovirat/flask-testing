from flask_restplus import Namespace, Resource, fields

api = Namespace('text_processing', description='space for ')

help_model = api.model('Info', {
    'info': fields.String(required=True, description='Help usage'),
})



help_text = "This endpoint blabla, Usage: blabla"

@api.route('/')
class TextProcessingOperations(Resource):
    @api.marshal_with(help_model)
    def get(self):
        return {'info': help_text}


@api.route('/count')
class TextProcessingCount(Resource):
    def post(self):
        return {'info': help_text}

@api.route('/count/word')
class TextProcessingCount(Resource):
    def post(self):
        return {'info': help_text}

@api.route('/count/character')
class TextProcessingCount(Resource):
    def post(self):
        return {'info': help_text}

# @api.route('/count/character/<letter:text>')
# class TextProcessingCount(Resource):
#     def post(self, letter):
#         return {'info': help_text}
