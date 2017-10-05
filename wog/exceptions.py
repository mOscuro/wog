# -*- coding: utf-8 -*-
"""List of possible messages with loc."""
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

from bb.translations import (ERROR_ENTITY_NOT_FOUND_F, ERROR_MISSING_PK_F,
                             ERROR_OPERATION_INVALID,
                             ERROR_OPERATION_INVALID_F,
                             ERROR_PARAMETER_INVALID_F,
                             ERROR_PARAMETER_INVALID_WITH_MESSAGE_F)


class BbValidationError(ValidationError):
    """
    Custom override of the ValidationError.
    Provides additional basic behaviour:
    - Always return a 400
    - Detail is auto-translated using a well-formatted string
    - If message or param is passed, the error messages are a bit different
    """

    def __init__(self, message: str = None, param: str = None):
        detail = ERROR_OPERATION_INVALID
        if message and param:
            detail = ERROR_PARAMETER_INVALID_WITH_MESSAGE_F.format(
                parameter=param, message=message)
        elif message:
            detail = ERROR_OPERATION_INVALID_F.format(message=message)
        elif param:
            detail = ERROR_PARAMETER_INVALID_F.format(parameter=param)
        super().__init__(detail, code=status.HTTP_400_BAD_REQUEST)


class BbNotFound(NotFound):
    """
    Custom override of the NotFound error.
    Provides additional basic behaviour:
    - Always return a 404
    - If pk is passed, then the error message includes the ID of the entity
    - Detail messages are auto-translated 
    """

    def __init__(self, entity: str, pk: str = None):
        detail = ''
        if pk:
            detail = ERROR_ENTITY_NOT_FOUND_F.format(
                entity=entity, id=pk)
        else:
            detail = ERROR_MISSING_PK_F.format(entity=entity)
        super().__init__(detail, code=status.HTTP_404_NOT_FOUND)
