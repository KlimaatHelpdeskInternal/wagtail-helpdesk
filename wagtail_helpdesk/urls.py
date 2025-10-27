from django.templatetags import static
from django.urls import include, path

from wagtail_helpdesk.cms.urls import urlpatterns as cms_urlpatterns
from wagtail_helpdesk.cms.views import js_wrapper

# Provide a single urls file for the whole project to make integration easier
urlpatterns = [
    path("", include(cms_urlpatterns)),
]

#urlpatterns += static('carboncalculator.js', js_wrapper, name = "carboncalculator.js")
