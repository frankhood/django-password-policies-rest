from django.http.response import Http404
from rest_framework import exceptions
from rest_framework import generics, authentication, permissions, renderers
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import set_rollback

from .permissions import IsActiveUser
from .serializers import PasswordPoliciesSerializer


def code_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.
    These Exceptions will return error codes instead of error message

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            # get the Error codes instead of Error messages
            data = exc.get_codes()
        else:
            data = {'detail': exc.get_codes()}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None


class ChangePasswordCheckAPIView(
    generics.GenericAPIView,
):
    authentication_classes = ()
    permission_classes = (
        permissions.AllowAny,
    )
    renderer_classes = (renderers.JSONRenderer, )
    serializer_class = PasswordPoliciesSerializer

    def get_exception_handler(self):
        """ Modify exception handler to return error codes instead of error strings """
        return code_exception_handler

    def post(self, request, *args, **kwargs):  # noqa
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "OK"})


