
from permissions.models import Permission
from permissions.serializers import PermissionSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PermissionsView(APIView):
    @staticmethod
    def get(request):
        try:
            user = request.user

            if not user:
                Response(
                    data={'error': 'Невалидный пользователь'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            permissions = Permission.objects.filter(user=user)
            serializedPermissions = PermissionSerializer(data=permissions, many=True)

            if not serializedPermissions.is_valid():
                Response(
                    data={'error': 'Невалидные права пользователя'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response(
                data=map(lambda p: p['key'], serializedPermissions.data),
                status=status.HTTP_200_OK
            )

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
