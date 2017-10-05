# -*- coding: utf-8 -*-
"""
Override of REST serializers to provide additional features such as:
- an EncryptedIdField to factorize encryption / decryption of the ID fields
- a Response serializer that makes all fields read_only
"""
from annoying.functions import get_object_or_None
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer

from bb.exceptions import BbNotFound
from bb.helpers import decrypt_id, encrypt_id, is_encrypted_id
from bb.translations import ERROR_PARAMETER_INVALID_F


# class EncryptedIdField(Field):
#     """
#     Define an ID Field that must be:
#     - encrypted in input and output
#     - decrypted when reaching the serializer validate code
#     - read_only (it is never possible to change the DB ID)

#     Currently, this Field is only available to ModelSerializer.
#     """
#     default_error_messages = {'invalid': ERROR_PARAMETER_INVALID_F.format(parameter='id'),}
#     initial = None

#     def to_internal_value(self, data):
#         self.read_only = True
#         if data is None:
#             return None
#         if not is_encrypted_id(data):
#             self.fail('invalid', input=data)
#         return decrypt_id(data)

#     def to_representation(self, value):
#         """Transform the id value to its encrypted form."""
#         return encrypt_id(value) if value is not None else None

class WogSerializer(ModelSerializer):
    """
    A ModelSerializer with extended features:
    - Utilities to retrieve PK kwargs and related objects
    - `optional_fields` class property to avoid making it in Meta
    - Utility method for rising Validation errors
    - a default encrypted `id` property that can be used by adding it in `fields`
    """ 
    # id = EncryptedIdField()
    optional_fields = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in set(self.optional_fields.keys()):
            self.fields[field_name].required = False

    def _get_pk_from_kwargs(self, name):
        return self.context['view'].kwargs.get('%s_pk' % name)

    def _get_object(self, klass, entity_name):
        pk = self._get_pk_from_kwargs(entity_name)
        if pk is None:
            raise NotFound()
        instance = get_object_or_None(klass=klass, id=pk)
        if instance is None:
            raise NotFound()
        return instance

    def get_user(self):
        if not hasattr(self, 'context') or not 'request' in self.context:
            return None
        return self.context['request'].user

class ResponseSerializerMixin():
    """A Mixin for serializers that makes all fields read_only."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in set(self.fields.keys()):
            self.fields[field_name].read_only = True

class WogResponseSerializer(WogSerializer, ResponseSerializerMixin):
    """A WogSerializer with Response attributes."""
    pass

class WogUpdateSerializer(WogSerializer):
    """A WogSerializer that makes all fields optional."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in set(self.fields.keys()):
            self.fields[field_name].required = False
