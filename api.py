import flask
import secrets

from datetime import datetime
from flask_rest_jsonapi import ResourceDetail

MAX_SECRET_LENGTH = 7
PASSWORD_EXPIRATION_TIME = 10


class Index(ResourceDetail):
    
    def get(self) -> dict:
        """Get method implementation that returns the current server status.
        """
        return {}

class ClientPassword(ResourceDetail):
    CLIENT_PASSWORDS = {}
    def get(self, id: int) -> dict:
        """Get method implementation that taking a one client identifier, it returns the password associated with it.
        Args:
            id : the client identifier.
        """
        client_info = None
        print (self.CLIENT_PASSWORDS)
        if id in self.CLIENT_PASSWORDS:
            client_info = self.CLIENT_PASSWORDS[id]
            current_time = datetime.now()
            time_delta = (current_time - client_info['updated'])
            if time_delta.total_seconds() > PASSWORD_EXPIRATION_TIME:
                client_info['password'] = secrets.token_hex(MAX_SECRET_LENGTH)
        else:
            client_info = {
                'updated': datetime.now(),
                'password': secrets.token_hex(MAX_SECRET_LENGTH)
            }
        
        return client_info