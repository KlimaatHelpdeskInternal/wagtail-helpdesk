
from wagtail_helpdesk.tenants.models import Tenant, EnvironmentURL
from django.core.exceptions import ImproperlyConfigured
from wagtail_helpdesk.tenants.models import Tenant, EnvironmentURL
from django.core.exceptions import ValidationError


def hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(':')[0].lower()


def tenant_from_request(request):
    #detect the hostname
    hostname = hostname_from_request(request)
    #then find the corresponding environment URL bij performing a lower case exact match
    foundenvironmenturl = EnvironmentURL.objects.filter(urlroot__iexact=hostname.lower()).first()
    if foundenvironmenturl is None:
            message = f"No environmentURL found for hostname '{hostname}'"
            raise ImproperlyConfigured(message)
    #then find the tenant that matches this environement
    foundtenant  = Tenant.objects.filter(environmenturl=foundenvironmenturl.id).first()
    if foundtenant is None:
            message = f"No tenant found for hostname '{hostname}'"
            raise ImproperlyConfigured(message)
    
    #return the id for the found tenant
    tenantid = foundtenant.id


    return tenantid

def is_admin_request(request):
    # detect if this is request to the admin module
    return request.path.startswith("/admin")

