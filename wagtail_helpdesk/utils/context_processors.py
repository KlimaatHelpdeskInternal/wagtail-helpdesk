import os
from django.conf import settings
from wagtail_helpdesk.cms.models import AnswerIndexPage, HomePage
from wagtail_helpdesk.tenants.models import Tenant
from apps.core.storages import MediaS3Storage



def settings_context(_request):
    return {"settings": settings}

def defaults(request):
    home_page = HomePage.objects.first()
    if home_page:
        menu_qs = home_page.get_children().live().in_menu()
    else:
        menu_qs = None
    answer_index_page = AnswerIndexPage.objects.first()


    tenantidstring = os.getenv("TENANTID", "-1")
    tenantid = int(tenantidstring)
    if tenantid>=0:
        tenant_info = Tenant.objects.first()
        sitename  = tenant_info.sitename
        favicon = tenant_info.favicon
        faviconurl =  "" if favicon is None or favicon.file is  None else favicon.file.url 
        logo = tenant_info.logo
        logourl = ""  if logo is None or logo.file is  None else logo.file.url
        logofooter = tenant_info.logofooter
        logofooterurl ="" if logofooter is None or logofooter.file is None else logofooter.file.url
    else:
        sitename = ""

    return {
        "main_nav": menu_qs,
        "answers_list_url": answer_index_page.url if answer_index_page else "",
        "sitename" : sitename,
        "logo_url" : logourl,
        "logo_footer_url" : logofooterurl,
        "favicon_url": faviconurl
    }
