from rest_framework.views import exception_handler
from rest_framework import permissions

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class IsNotOwner(permissions.IsAuthenticated):
    """
    Object-level permission to disallow owners of an object.
    If the view has not attribute `get_onwer` with instance parameter, 
    it is assumed that ownership is not granted.
    """
    def has_object_permission(self, request, view, instance):
        # Instance must have an attribute named `owner`.
        if getattr(view, 'get_owner', None):
            return view.get_owner(instance) != request.user
        return True
