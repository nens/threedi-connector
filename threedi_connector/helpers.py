from collections import namedtuple
import getpass

from .compat import raw_input

Credentials = namedtuple('Credentials', ['username', 'password'])


def get_credentials_interactively():
    username = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    return Credentials(username, password)
