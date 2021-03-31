from rest_framework import authentication


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        pass