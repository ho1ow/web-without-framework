import bcrypt
from dotenv import load_dotenv
import os
load_dotenv()

salt = os.getenv('SALT').encode('utf-8')


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
