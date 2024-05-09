import os
import jwt
from dotenv import load_dotenv
load_dotenv()
SECRET = os.getenv('SECRET')



def generate_token(data):
    return jwt.encode(data, SECRET, algorithm='HS256')

def verify_token(token):
    return jwt.decode(token, SECRET, algorithms=['HS256'])
def verify_user(self):
    if 'Cookie' not in self.headers:
        return None
    token = self.headers['Cookie'].split('=')[1]
    return verify_token(token)['username']
