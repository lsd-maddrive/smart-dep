import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

import jwt

def decode_token(token, secret, alg='HS256'):
    """
        Decodes the auth token
        Args: 
            token: encoded token (payload)
            secret: secret (string)
            alg: encoding algorithm
        Returns:
            user ID (integer)
            time of creation token (int) = number of seconds
    """
    try:
        payload = jwt.decode(token, secret, algorithms=[alg])
        return payload['user'], payload['iat']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.', ''
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.', ''

    
def encode_token(user_id, created_time, expired_time, secret):
        """
            Generates the Auth Token
            Args:
                user_id(integer): parent ID 
            Returns: 
                token (string)
        """
        try:
            header = {
                'typ': 'JWT', 
                'alg': 'HS256'
            }

            payload = {
                # the subject of the token 
                'sub': "auth", 
                # expiration date of the token
                'exp': expired_time,
                # the time the token is generated
                'iat': created_time,
                # user who receive the token 
                'user': user_id,
            }

            token = jwt.encode(
                payload,
                secret,
                algorithm=header['alg']
            )
            # convert from bytes to string 
            return token.decode('utf-8')
       
        except Exception as err:
            logger.error(f"Encode Token Payload Error {err}")
            return err

    