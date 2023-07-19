from django.views.generic import TemplateView


class SwaggerView(TemplateView):
    template_name = 'swagger-ui.html'
    extra_context = {'schema_url': 'openapi-schema'}
