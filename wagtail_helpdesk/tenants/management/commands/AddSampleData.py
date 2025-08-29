from django.core.management.base import BaseCommand, CommandError

from django.core.exceptions import ValidationError
from wagtail_helpdesk.utils.datamanager import add_new_tenant, add_EnvironmentURL
from wagtail_helpdesk.tenants.models import Tenant, EnvironmentURL
from wagtail_helpdesk.cms.models import HomePage



class Command(BaseCommand):
    help = "Creates a new based on a template tenant"

    def handle(self, *args, **options):
            template_id = 0
            newtenant_id = 1

            newtenant = add_new_tenant(self,template_id, template_id, "TempTenantName","TempTenantDescription")
            #add the new EnvironmentURL
            add_EnvironmentURL(self,newtenant, "NewEnvironment", "KlimaatHelpdeskLocalDE" )
            
            #create a new homepage
            templatetenant = Tenant.objects.get(id=template_id)
            #first find out current homepage 
            currenthomepage  = HomePage.objects.first()
            currenthomepage.tenantid.add(templatetenant)
            pageid = currenthomepage.id

            newhomepage = currenthomepage.copy(recursive=False, copy_revisions=False, keep_live=False, update_attrs={'slug': 'NewSlug'})
            newhomepage.save()
            newhomepage.tenantid.add(newtenant)
            self.stdout.write(self.style.SUCCESS('Created a new homepage'))


            self.stdout.write(self.style.SUCCESS('Successfully created sample data'))
