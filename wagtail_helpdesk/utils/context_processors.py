import os
from django.conf import settings
from wagtail_helpdesk.cms.models import AnswerIndexPage, HomePage
from apps.core.storages import MediaS3Storage
from wagtail.models import Site
from wagtail_helpdesk.site_settings.models import SiteSettings



def settings_context(_request):
    return {"settings": settings}

def defaults(request):
    site = Site.find_for_request(request)
    
    if (site is not None):
        home_page = site.root_page
    else:
        home_page = HomePage.objects.first()
        
    if home_page:
        menu_qs = home_page.get_children().live().in_menu()
    else:
        menu_qs = None
    answer_index_page = AnswerIndexPage.objects.first()


    if site is not None:
        siteid = site.id
    else:
        siteid = -1
    if siteid>=0:
        sitesettings = SiteSettings.for_request(request=request)
        sitename  = sitesettings.sitename
        favicon = sitesettings.favicon
        faviconurl =  "" if favicon is None or favicon.file is  None else favicon.file.url 
        logo = sitesettings.logo
        logourl = ""  if logo is None or logo.file is  None else logo.file.url
        logofooter = sitesettings.logofooter
        logofooterurl ="" if logofooter is None or logofooter.file is None else logofooter.file.url
        css_file_name = sitesettings.css_file_name
        baseurl = site.root_url
        return {
            "main_nav": menu_qs,
            "answers_list_url": answer_index_page.url if answer_index_page else "",
            "sitename" : sitename,
            "logo_url" : logourl,
            "logo_footer_url" : logofooterurl,
            "favicon_url": faviconurl,
            "site_id" : siteid,
            "css_file_name" : 'wagtail_helpdesk/' + css_file_name,
            "base_url" : baseurl

        }
        
    else:
        return {
            "main_nav": menu_qs,
        }

