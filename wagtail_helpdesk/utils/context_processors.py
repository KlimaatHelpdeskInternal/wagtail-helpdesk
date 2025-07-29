from django.conf import settings
from responses import logger

from wagtail_helpdesk.cms.models import AnswerIndexPage, HomePage
from wagtail_helpdesk.tenants.utils import tenant_from_request
from django.core.exceptions import ImproperlyConfigured


def settings_context(_request):
    return {"settings": settings}


def defaults(request):
    foundtenantid = tenant_from_request(request)
    home_page = HomePage.objects.filter(tenantid=foundtenantid).first()
    if home_page is None:
            message = f"No home_page defined for this tenant {foundtenantid}"
            raise ImproperlyConfigured(message)
    logger.debug(f"Found tenant id for homepage {foundtenantid}")
    
    logger.info("Read defaults in utils/context_processors")

    if home_page:
        menu_qs = home_page.get_children().live().in_menu()
    else:
        menu_qs = None
    answer_index_page = AnswerIndexPage.objects.first()
    if answer_index_page is None:
            message = f"No answer_index_page defined for this tenant {foundtenantid}"
            raise ImproperlyConfigured(message)
    return {
        "main_nav": menu_qs,
        "answers_list_url": answer_index_page.url if answer_index_page else "",
    }
