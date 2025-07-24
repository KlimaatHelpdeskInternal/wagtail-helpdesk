
from wagtail_helpdesk.tenants.models import Tenant, EnvironmentURL
from django.core.exceptions import ImproperlyConfigured

def hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(':')[0].lower()


def tenant_from_request(request):
    hostname = hostname_from_request(request)
    environmenturl = EnvironmentURL.objects.filter(urlroot__iexact=hostname.lower()).first()
    if environmenturl is None:
            message = f"No tenant found for hostname '{hostname}'"
            raise ImproperlyConfigured(message)
    tenantid = environmenturl.id


    return tenantid#Tenant.objects.filter(subdomain_prefix=subdomain_prefix).first()