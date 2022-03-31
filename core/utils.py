from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

class JWTTokens:
    REFRESH_TOKEN_KEY = 'refreshToken'
    ACCESS_TOKEN_KEY = 'accessToken'

    def getTokenForUser(user):
        refreshToken = RefreshToken.for_user(user)

        tokens = {}
        tokens[JWTTokens.REFRESH_TOKEN_KEY] = str(refreshToken)
        tokens[JWTTokens.ACCESS_TOKEN_KEY] = str(refreshToken.access_token)

        return tokens

    def updateTokens(refreshToken):
        refreshToken = RefreshToken(refreshToken)
        
        tokens = {}
        tokens[JWTTokens.REFRESH_TOKEN_KEY] = str(refreshToken)
        tokens[JWTTokens.ACCESS_TOKEN_KEY] = str(refreshToken.access_token)

        return tokens

    def setRefreshTokenToCookie(response, refreshToken):
        response.set_cookie(
            key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
            value = refreshToken,
            expires = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

    def addAccessTokenToResponse(response, accessToken):
        if response.data == None:
            response.data = {}
        
        response.data[JWTTokens.ACCESS_TOKEN_KEY] = accessToken

    def setTokensToResponse(response, tokens):
        JWTTokens.setRefreshTokenToCookie(response, tokens[JWTTokens.REFRESH_TOKEN_KEY])
        JWTTokens.addAccessTokenToResponse(response, tokens[JWTTokens.ACCESS_TOKEN_KEY])