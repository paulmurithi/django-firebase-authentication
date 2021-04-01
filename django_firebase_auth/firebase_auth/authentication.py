"""
A module to authenticate users using firebase
"""

import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework import status

from django.contrib.auth import get_user_model
from django.conf import settings

# initialize firebase app
cred = credentials.certificate('/home/programmer/Downloads/grodigi-d809f-firebase-adminsdk-bgxm4-61f5bf15b9.json')
default_app = firebase_admin.initialize_app(cred)


class FirebaseAuthentication(BaseAuthentication):
    """
    A class to authenticate users using firebase
    extends drf BaseAuthentication class
    """

    def authenticate(self, request):
        """
        A method to authenticate users using firebase
        Impletments Authenticate abstract method of the BaseAuthentication class
        
        parameters:
            -id_token
        response:
            -request.user instanse
            -request.auth instance
        """

        auth_header = request.META.get("HTTP_AUTHORIZATION", None)
        if not auth_header:
            raise ValidationError("No auth token provided", status.HTTP_400_BAD_REQUEST)
        
         # Validate Authorization header schema
        schema = settings['FIREBASE_AUTH_HEADER_SCHEMA']
        if not auth_header.startswith('{schema} '.format(schema=schema)):
            raise ValidationError("Authorization header does not start with 'Bearer'", status.HTTP_400_BAD_REQUEST)

        # pop the id_token
        # Bearer eiiiiivfbsdvgvjfdfkmldkk8940980mlkefb
        id_token = auth_header.split(" ").pop()
        decoded_token = None

        check_revoked = settings['FIREBASE_ALLOW_REVOKED']

        try:
            """
            decoded string properties
                -aud
                -auth_time
                -email
                -email_verified
                -exp
                -firebase
                -iat
                -iss
                -phone_number
                -picture
                -sub
                -uid
            """

            # verify id_token
            decoded_token = auth.verify_id_token(id_token, check_revoked=check_revoked)

            # Disallow unverified Emails if flag is set
            if (not settings['FIREBASE_ALLOW_UNVERIFIED_EMAIL'] and not decoded_token['email_verified']):
                raise AuthenticationFailed("Email not verified")

        except Exception:
            raise AuthenticationFailed("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
            phone_number = decoded_token.get("phone_number")
        except Exception:
            raise AuthenticationFailed("Invalid auth token")

        # get or create a user if doesn't exist
        user, created = get_user_model().objects.get_or_create(username=uid, phone_number=phone_number)
        return (user, None)
