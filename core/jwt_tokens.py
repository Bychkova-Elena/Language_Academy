from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


class JWTTokens:
    REFRESH_TOKEN_KEY = settings.SIMPLE_JWT['AUTH_COOKIE']
    ACCESS_TOKEN_KEY = 'accessToken'

    @staticmethod
    def GetTokensByUser(user) -> dict:
        refreshToken = RefreshToken.for_user(user)

        tokens = {}
        tokens[JWTTokens.REFRESH_TOKEN_KEY] = str(refreshToken)
        tokens[JWTTokens.ACCESS_TOKEN_KEY] = str(refreshToken.access_token)

        return tokens

    @staticmethod
    def GetNewTokens(refreshToken) -> dict:
        refreshToken = RefreshToken(refreshToken)

        tokens = {}
        tokens[JWTTokens.REFRESH_TOKEN_KEY] = str(refreshToken)
        tokens[JWTTokens.ACCESS_TOKEN_KEY] = str(refreshToken.access_token)

        return tokens

    @staticmethod
    def AddRefreshTokenToCookie(response, refreshToken) -> None:
        response.set_cookie(
            key=JWTTokens.REFRESH_TOKEN_KEY,
            value=refreshToken,
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

    @staticmethod
    def AddAccessTokenToResponse(response, accessToken) -> None:
        if response.data is None:
            response.data = {}

        response.data[JWTTokens.ACCESS_TOKEN_KEY] = accessToken

    @staticmethod
    def AddTokensToResponse(response, tokens) -> None:
        JWTTokens.AddRefreshTokenToCookie(response, tokens[JWTTokens.REFRESH_TOKEN_KEY])
        JWTTokens.AddAccessTokenToResponse(response, tokens[JWTTokens.ACCESS_TOKEN_KEY])

    @staticmethod
    def OutdateTokens(refreshToken) -> None:
        tokens = RefreshToken(refreshToken)
        tokens.blacklist()
