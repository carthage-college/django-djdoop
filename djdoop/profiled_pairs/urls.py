from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djdoop.profiled_pairs.views',
    url(
        r'^success/$',
        TemplateView.as_view(
            template_name='profiled_pairs/success.html'
        ),
        name='profiled_pairs_success'
    ),
    url(
        r'^(?P<stype>[a-zA-Z0-9_-]+)/$',
        'form', name="profiled_pairs_form"
    ),
)
