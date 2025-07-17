from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TenantsConfig(AppConfig):
    name = "wagtail_helpdesk.tenants"
    verbose_name = _("Tenants")
