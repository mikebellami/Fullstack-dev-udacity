import json
from jose import jwt
from urllib.request import urlopen

# Configuration
# UPDATE THIS TO REFLECT YOUR AUTH0 ACCOUNT
AUTH0_DOMAIN = 'bellay-fsnd.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# MAKE SURE THIS IS A VALID AUTH0 TOKEN FROM THE LOGIN FLOW
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ild6S1BMYzVzSUZIX241RUhucEk1TiJ9.eyJpc3MiOiJodHRwczovL2JlbGxhbXktZnNuZC5ldS5hdXRoMC5jb20vIiwic3ViIjoiekxHVzNrNmR1R1lham1vcXo4RFJLZnRtc3lyaG45YWVAY2xpZW50cyIsImF1ZCI6ImltYWdlIiwiaWF0IjoxNjU4NTkyMzEwLCJleHAiOjE2NTg2Nzg3MTAsImF6cCI6InpMR1czazZkdUdZYWptb3F6OERSS2Z0bXN5cmhuOWFlIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.H5E8iDXJUGMY6YOeeifn-AfdtZeJNon0iN2wuljG13lQcFEa0g7LNU2HegnzcylZMs4aCRgv9ue9T-HkmwJhuhlQk1Rm6iQANgcDyrydonaa4l96AoRz_88kDN0TIkD_HZ3MD1NZ_Wm4YQp_2otGBFk1VBoKux8DQ0ByzWltjLT91q91y_w15P7wi_gF_vxHzu4rtZqFZBzxJAjL7FkvVcMsYR2wTSak8oFI9XqjjXgcWwdTBMaSWFIZ_2uKdQC-pXrKk2YwrnzctA0jKqBv8OC9ayaVbx_sI03JCn7ZPMg9DrrdaIJnFgd0qFV5VsF4Zqxg8c8UPsVvJPbvsa7OnQ"

## Auth Header
def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    
    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)