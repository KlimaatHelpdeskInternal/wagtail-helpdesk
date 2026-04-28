from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from wagtail_helpdesk.tenants.models import Tenant




class TenantAdmin(ModelAdmin):
    model = Tenant
    menu_label = _("Tenants")
    menu_icon = "user"
    menu_order = 280
    add_to_settings_menu = False
    exclude_from_explorer = False


modeladmin_register(TenantAdmin)

admin.site.register(
    [
        Tenant,
    ]
)
