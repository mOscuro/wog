# -*- coding: utf-8 -*-
"""
Override of REST viewsets to provide additional features such as:
- a different serializer for the response
- more meaningful class properties
- custom headers
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet


class WogViewSet(GenericViewSet):
    """Customized ViewSet for our project."""
    permission_classes = (IsAuthenticated,)
    response_serializer_class = None

    def get_response(self, status: int, *args, **kwargs):
        """Utility to construct the Response to a Request."""
        # Retrieve the Serializer
        serializer_class = self.get_serializer_class(True)
        kwargs['context'] = self.get_serializer_context()
        serializer = serializer_class(*args, **kwargs)

        # Construct the Response
        headers = self._get_response_headers(serializer.data)
        return Response(data=serializer.data, status=status, headers=headers)

    def _get_response_headers(self, data):
        """Add default headers to the Response."""
        # 'content-type': ~ 'application/json; %s' % ApiVersion.get_content_type()
        headers = {}
        try:
            # TODO: add our custom headers here (ie. 'version')
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            pass
        return headers

    def get_serializer_class(self, is_response: bool = False):
        """
        Override the `get_serializer_class` method of the `GenericViewSet`
        class from rest_framework to add some understandable logic.
        Params:
        - is_response: whether the serializer is intended for Response
        """
        if is_response:
            serializer_class = self.get_specific_response_serializer()
            if serializer_class:
                return serializer_class
            assert self.response_serializer_class is not None
            return self.response_serializer_class
        return self.get_specific_request_serializer()\
        or super().get_serializer_class()

    def get_specific_response_serializer(self, *args, **kwargs):
        """
        Can be used to add a specific response serializer.
        This behaviour should be added in the Mixins only.
        """
        if self.action == 'retrieve':
            return self.retrieve_serializer_class
        return None

    def get_specific_request_serializer(self, *args, **kwargs):
        """
        Can be used to add a specific request serializer.
        This behaviour should be added in the Mixins only.
        """
        if self.action == 'destroy':
            return self.destroy_serializer_class
        if self.action == 'create':
            assert self.create_serializer_class is not None
            return self.create_serializer_class
        if self.action == 'partial_update':
            assert self.update_serializer_class is not None
            return self.update_serializer_class
        return None
