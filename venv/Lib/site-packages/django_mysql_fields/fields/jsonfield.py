import json

from django.core import exceptions
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_mysql_fields import forms


class JSONField(models.Field):
    """
    JSONField based on Django's contrib Postgres JSONField field.
    """
    empty_strings_allowed = False
    description = _('A JSON object')
    default_error_messages = {
        'invalid': _("Value must be valid JSON."),
    }

    def db_type(self, connection):
        return 'mediumtext'

    def from_db_value(self, value, expression, connection, context):
        if not value:
            return

        return json.loads(value)

    def get_prep_value(self, value):
        if value is not None:
            return json.dumps(value)

        return value

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        try:
            json.dumps(value)
        except TypeError:
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def value_to_string(self, obj):
        value = self.value_from_object(obj)

        return value

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.JSONField}
        defaults.update(kwargs)

        return super().formfield(**defaults)
