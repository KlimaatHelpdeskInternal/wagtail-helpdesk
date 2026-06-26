from django.conf import settings
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic.base import TemplateView
from wagtail_helpdesk.cms.models import AnswerCategory, AnswerIndexPage, Answer, Expert, ExpertAnswerOverviewPage, ExpertIndexPage, Volunteer, VolunteerIndexPage, AnswerOriginBlock
from wagtail.models import Orderable, Page
from wagtail_helpdesk.site_settings.models import SiteSettings
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator



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




class AnswersListView(TemplateView):
    '''A new view that helps to list the answers filtered for a specific site'''
    template_name = "wagtail_helpdesk/cms/answers_list.html"
    context_object_name = 'answers_and_columns'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            sitesettings=SiteSettings.for_request(request=self.request)
            sitesettingsavailable = True
        except Exception as e:
            sitesettings = None
            sitesettingsavailable = False
        filteredanswers = Answer.objects.live()
        #if sitesettings is not None:
        #    filteredanswers = filteredanswers.filter(siteid__in=[sitesettings.site_id])

        answers = (
            filteredanswers
            .filter(type="answer")
            .specific()
            .order_by("-first_published_at")
        )
        columns = (
            Answer.objects.live()
            .filter(type="column")
            .specific()
            .order_by("-first_published_at")
        )

        # Search
        search = self.request.GET.get("search", "").strip()
        context["search"] = search
        if search:
            answers = answers.search(search).get_queryset()
            columns = columns.search(search).get_queryset()

        # Filter categories based on GET params
        chosen_categories = []
        for filter in self.request.GET:
            try:
                category = AnswerCategory.objects.get(name__iexact=filter)
            except AnswerCategory.DoesNotExist:
                # In case someone puts weird stuff in the url
                pass
            else:
                chosen_categories.append(category)

        if len(chosen_categories) > 0:
            answers = answers.filter(
                answer_category_relationship__category__in=chosen_categories
            )
            columns = columns.filter(
                answer_category_relationship__category__in=chosen_categories
            )

        # Adjust categories to maintain checked status
        categories = AnswerCategory.objects.all()
        categories_context = [
            {"category": c, "selected": True if c in chosen_categories else False}
            for c in categories
        ]

        # Insert column every 3 answers
        answers_and_columns = list(answers)
        if len(columns) > 0:
            # INTERSPACING = len(answers) // len(columns) # Can be used to spread evenly if desired
            INTERSPACING = 3
            if len(answers) >= INTERSPACING:
                column_index = 0
                for index in range(len(answers)):
                    if index != 0 and index % INTERSPACING == 0:
                        try:
                            answers_and_columns.insert(
                                index + column_index, columns[column_index]
                            )
                        except IndexError:
                            break
                        else:
                            column_index += 1
            # List is too short, cannot interspace, so just put them at the end
            else:
                answers_and_columns += list(columns)
        
        #list created, now paginate
        paginator = Paginator(answers_and_columns,25)
        page = self.request.GET.get("page")
        try:
            paginated_answers_and_columns = paginator.page(page)
            currentpage = int(page)
        except PageNotAnInteger:
            paginated_answers_and_columns = paginator.page(1)
            currentpage = 1 
        except EmptyPage:
            paginated_answers_and_columns = paginator.page(paginator.num_pages)
            currentpage = paginator.num_pages


        context.update(
            {
                "current_page": currentpage,
                "answers_page": AnswerIndexPage.objects.first().url,
                "categories": categories_context,
                "answers_and_columns": paginated_answers_and_columns,
                "experts_page": ExpertIndexPage.objects.first(),
            }
        )
        return context

class AnswerView(TemplateView):
    '''This view shows the answers for an answers that is listed in pultiple sites. The route to this view is added in urls.py'''
    template_name = "wagtail_helpdesk/cms/answer_detail.html"
    context_object_name = 'self'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answer = Answer.objects.filter(slug = context["slug"]).first()
        context["references"] = answer.get_references()
        context["self"] = answer

        return context
    
    
class ExpertView(TemplateView):
    '''This view shows the experts. We use a view to make sure if is displayed in multiple sites and we can add the route to this view in urls.py.'''
    template_name = "wagtail_helpdesk/experts/experts_list.html"
    
    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        experts = Expert.objects.all()
        categories = AnswerCategory.objects.all()
        itemsperpage = 25
        if self.request.GET.get("expertID") is not None :
            try:
                requestedexpertid = int( self.request.GET.get("expertID"))
                expertids = list(experts.values_list('id', flat = True))
                experttoopenwithindex= expertids.index(requestedexpertid)
                pagettoopenwith = 1 + experttoopenwithindex // itemsperpage # find the first page that contains the iddex of this expert

            except ValueError:
                pagettoopenwith = 1
                requestedexpertid = 0
        else :
            requestedexpertid = 0
            pagettoopenwith = 1 


        #list created, now paginate
        paginator = Paginator(experts,itemsperpage)
        if  self.request.GET.get("page") is not None :
            page =  self.request.GET.get("page")
        else :
            page = pagettoopenwith

        try:
            paginated_experts = paginator.page(page)
            currentpage = int(page)
        except PageNotAnInteger:
            paginated_experts = paginator.page(1)
            currentpage = 1 
        except EmptyPage:
            paginated_experts = paginator.page(paginator.num_pages)
            currentpage = paginator.num_pages


        context.update(
            {
                "experts": paginated_experts,
                "answers_page": AnswerIndexPage.objects.first().url,
                "expert_answers_page": ExpertAnswerOverviewPage.objects.first(),
                "categories": categories,
                "current_page" : currentpage,
            }
        )
        return context

class VolunteerView(TemplateView):
    '''This view shows the volunteers. We use a view to make sure if is displayed in multiple sites and we can add the route to this view in urls.py.'''
    template_name = "wagtail_helpdesk/volunteers/volunteers_list.html"
    
    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        volunteers = Volunteer.objects.all()

        context.update(
            {
                "volunteers": volunteers,
            }
        )
        return context

