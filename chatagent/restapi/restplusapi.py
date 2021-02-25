import sys
import traceback
from flask_restplus import Api

from restapi.ChatException import ChatException, InternalServerError


class CustomApi(Api):

    def handle_error(self, error):

        if isinstance(error, ChatException):
            return self.make_response(error.__dict__, error.status)

        code = getattr(error, 'code', 500)

        if code == 400:
            try:
                data = getattr(error, 'data', str(error))
                response = {'status': code}
                ####To check if exception is custom exception or not (custom exception for input validation has dict structure)
                if isinstance(data, str):
                    response['title'] = data
                    response['detail'] = data
                else:
                    response['title'] = data['message']
                    response['errors'] = []
                    errors = data['errors']
                    
                    for key in errors:
                        param_error = {'title': 'Invalid Parameter', 'detail': key + ' : ' + errors[key]}
                        response['errors'].append(param_error)

                return self.make_response(response, 400)
                
            except(Exception):
                traceback.print_exc(file=sys.stdout)
                return self.make_response({'title': 'Payload validation failed.',
                                           'detail': 'Payload validation failed.', 'status': 400},
                                          400)

        elif code == 404:
            return self.make_response({'title': 'Not Found',
                                       'detail': 'The requested URL was not found on the server.  If you entered the '
                                                 'URL manually please check your spelling and try again.',
                                       'status': 404}, 404)

        elif code == 500:
            return self.make_response({'title': 'Internal Server Error',
                                       'detail': 'Request failed due to Internal Server Error.', 'status': 500},
                                      500)

        return super(CustomApi, self).handle_error(error)


api = CustomApi(version='0.1', title='Chat Service',
                description='Chat Service', catch_all_404s=True)