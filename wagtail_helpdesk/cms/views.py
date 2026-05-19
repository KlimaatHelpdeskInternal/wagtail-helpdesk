from django.conf import settings
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic.base import TemplateView
from wagtail_helpdesk.cms.models import AnswerIndexPage, Answer
from wagtail.models import Orderable, Page



@xframe_options_exempt
def iframe_search_widget(request):
    return render(
        request,
        "wagtail_helpdesk/cms/iframe_search_widget.html",
        {
            "title": request.GET.get("title", _("Search")),
            "answers_page": f"{settings.WAGTAILADMIN_BASE_URL}{AnswerIndexPage.objects.first().url}",
            "base_url": settings.WAGTAILADMIN_BASE_URL,
        },
    )

def js_wrapper(request):
    django_var = "a message to js"
    context_for_js = {'django_var ': django_var}
    return render(request, 'templates-wagtail/helpdesk/cms/carboncalculator.js', context_for_js ,"application/javascript")





class AnswerView(TemplateView):
    template_name = "wagtail_helpdesk/cms/answer_detail.html"
    context_object_name = 'self'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answer = Answer.objects.filter(slug = context["slug"]).first()
        context["self"] = answer
        return context