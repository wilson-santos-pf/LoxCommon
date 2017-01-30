from base64 import b16encode
from hashlib import sha512
from os import urandom


def get_password_hash_with_salt(password, salt=None):
    """
    Get a password hashed with a salt.

    :param password:
    :param salt:
    :return: tuple (password_hashed, salt)
    """
    if salt is None:
        # TODO: use Crypto random instead
        salt = b16encode(urandom(8))
    pass_hash = sha512(str(salt) + password).hexdigest()
    return pass_hash, salt
