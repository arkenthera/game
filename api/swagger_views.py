from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes, schema
from rest_framework import response, schemas


@api_view()
@schema(None)
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Leaderboard API')
    return response.Response(generator.get_schema(request=request))
