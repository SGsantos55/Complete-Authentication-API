from rest_framework.renderers import JSONRenderer
from collections import OrderedDict

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = OrderedDict()

        response = renderer_context.get('response', None)
        status_code = response.status_code if response else 200
        response_data['status_code'] = status_code

        if isinstance(data, dict):
            non_field_errors = data.pop('non_field_errors', None)

            if non_field_errors:
                # Add a custom message key for clarity
                response_data['message'] = non_field_errors[0]

            if data:
                response_data['errors'] = data
        else:
            response_data['data'] = data

        return super().render(response_data, accepted_media_type, renderer_context)
