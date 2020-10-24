import json

from django.forms import widgets


class FormattedJsonWidget(widgets.Textarea):
    """
    Overrides JSONField form widget to display formatted JSON text.
    """
    def render(self, name, value, attrs=None):
        value = json.dumps(json.loads(value), indent=2)

        return super().render(name, value, attrs)
