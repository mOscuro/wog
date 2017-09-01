# -*- coding: utf-8 -*-
"""
Override of REST mixins to provide additional features such as:
- a different serializer for the response
- more meaningful class properties
- only PATCH (no PUT)
"""
from rest_framework import status


class RetrieveMixin():
    """Add support for the GET method on an item with an ID, to the `WogViewSet`."""
    retrieve_serializer_class = None

    def retrieve(self, request, *args, **kwargs):
        """Handle a `retrieve` action in rest_framework."""
        # Serialize and package the response
        instance = self.get_object()
        self.validate_retrieve_authorization(instance)
        return self.get_response(status.HTTP_200_OK, instance)

    def validate_retrieve_authorization(self, instance) -> None:
        """
        Can be overriden to perform additional checks on the RETRIEVE action.
        When not valid, this method should Throw.
        """

class ListMixin():
    """Add support for the GET method on a list of items, to the `WogViewSet`."""

    def list(self, request, *args, **kwargs):
        """Handle a `list` action in rest_framework."""
        # Retrieve the existing objects
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        # Serialize the items and package the response
        return self.get_response(status.HTTP_200_OK, queryset, many=True)

class CreateMixin():
    """Add support for the POST method to the `WogViewSet`."""
    create_serializer_class = None

    def create(self, request, *args, **kwargs):
        """Handle a `create` action in rest_framework."""
        data = request.data
        self.validate_create_authorization(data)

        # Validate and create
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance, created = self.perform_create(serializer)

        # Serialize and package the response
        self.after_create(instance)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return self.get_response(status_code, instance)

    def perform_create(self, serializer) -> tuple:
        """
        Usually create an object. Can be used to return an existing object instead.
        Return a tuple (obj, created)."""
        return (serializer.save(), True)

    def after_create(self, instance) -> None:
        """Can be used to send mails or WebSocket messages."""

    def validate_create_authorization(self, data) -> None:
        """
        Can be overriden to perform additional checks on the CREATE action.
        When not valid, this method should Throw.
        """

class UpdateMixin():
    """Add support for the PATCH method only (no PUT) to the `WogViewSet`."""
    update_serializer_class = None

    def partial_update(self, request, *args, **kwargs):
        """Handle a `partial_update` action in rest_framework."""
        # Retrieve the existing object
        instance = self.get_object()
        self.validate_update_authorization(instance)

        # Validate and update
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)

        # Serialize and package the response
        self.after_update(instance)
        return self.get_response(status.HTTP_200_OK, instance)

    def perform_update(self, serializer) -> object:
        """Perform the update and return the updated item."""
        return serializer.save()

    def after_update(self, instance) -> None:
        """Can be used to send mails or WebSocket messages."""

    def validate_update_authorization(self, instance) -> None:
        """
        Can be overriden to perform additional checks on the UPDATE action.
        When not valid, this method should Throw.
        """

class DestroyMixin():
    """Add support for the DELETE method to the `WogViewSet`."""
    destroy_serializer_class = None

    def destroy(self, request, *args, **kwargs):
        """Handle a `destroy` action in rest_framework."""
        instance = self.get_object()
        self.validate_destroy_authorization(instance)
        if self.destroy_serializer_class:
            # Custom destroy logic using a serializer
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            saved = serializer.save()
            self.after_destroy(saved)
            return self.get_response(status.HTTP_200_OK, saved)
        # Usual destroy logic
        self.perform_destroy(instance)
        self.after_destroy(None)
        return self.get_response(status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance) -> None:
        """Actually delete the item."""
        instance.delete()

    def after_destroy(self, instance) -> None:
        """
        Can be used to send mails or WebSocket messages.
        `instance` should be None if is has been destroyed.
        """

    def validate_destroy_authorization(self, instance) -> None:
        """
        Can be overriden to perform additional checks on the DELETE action.
        When not valid, this method should Throw.
        """
