import uuid

from django.db import models


class UUIDField(models.UUIDField):
    """
    Overrides Django UUIDField to store full UUID's including dashes.
    """
    def __init__(self, verbose_name=None, **kwargs):
        super().__init__(verbose_name, **kwargs)
        self.max_length = 36

    def get_internal_type(self):
        return "CharField"

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value)
            except AttributeError:
                raise TypeError(self.error_messages['invalid'] % {'value': value})

        if connection.features.has_native_uuid_field:
            return value
        return str(value)
