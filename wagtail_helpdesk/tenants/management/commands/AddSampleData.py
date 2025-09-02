import time
import asyncio
from django.core.management.base import BaseCommand, CommandError

from django.core.exceptions import ValidationError
from wagtail_helpdesk.experts.models import Expert
from wagtail_helpdesk.utils.datamanager import add_new_tenant
from wagtail_helpdesk.tenants.models import Tenant, EnvironmentURL
from wagtail_helpdesk.cms.models import Answer, HomePage
from wagtail_helpdesk.volunteers.models import Volunteer
from googletrans import Translator


async def translate_text(inputtext, srclanguage, targetlanguage):
      async with Translator() as translator:
            result =await translator.translate( text=inputtext,src=srclanguage, dest=targetlanguage)
            print(result)
            return result.text

class Command(BaseCommand):
    help = "Creates a new based on a template tenant"

    def handle(self, *args, **options):
            template_id = 0
            newtenant_id = 1

            #clear old tenants
            Tenant.objects.all().delete()
            #create base tenant
            defaulttenant = Tenant(id = 0, name = "KlimaatHelpdesk NL", description = "The dutch KlimaatHelpdesk")
            defaulttenant.save()

            #set all pages to this base tenant
            allanswers = Answer.objects.all()
            for tmpanswer in allanswers:
                  tmpanswer.tenantid.set([defaulttenant])
            
            #set all experts to this base tenant
            allexperts = Expert.objects.all()
            for tmpexpert in allexperts:
                  tmpexpert.tenantid.set([defaulttenant])

            #set all Volunteers to this base tenant
            allvolunteers = Volunteer.objects.all()
            for tmpvolunteer in allvolunteers:
                  tmpvolunteer.tenantid.set([defaulttenant])


            #now create a new tenant
            newtenant = add_new_tenant(self,template_id, newtenant_id, "TempTenantName","TempTenantDescription")
            
            #add the new EnvironmentURL's
            EnvironmentURL.objects.all().delete()
            new_list2 =[]
            newtenant.environmenturl.set(new_list2)
            new_list =[]
            defaulttenant.environmenturl.set(new_list)
            newenvironmenturl0 = EnvironmentURL(id = 0, name = "KlimaatHelpdeskNLLocal", urlroot="127.0.0.1")
            newenvironmenturl0.save()
            defaulttenant.environmenturl.add(newenvironmenturl0)
            newenvironmenturl1 = EnvironmentURL(id = 1, name = "KlimaatHelpdeskProd", urlroot="klimaathelpdesk.org")
            newenvironmenturl1.save()
            defaulttenant.environmenturl.add(newenvironmenturl1)
            newenvironmenturl2 = EnvironmentURL(id = 2, name = "KlimaatHelpdeskLocalDev", urlroot="KlimaatHelpdeskLocalNL")
            newenvironmenturl2.save()
            defaulttenant.environmenturl.add(newenvironmenturl2)
            newenvironmenturl3 = EnvironmentURL(id = 3, name = "KlimaatHelpdeskLocalDevGerman", urlroot="KlimaatHelpdeskLocalDE")
            newenvironmenturl3.save()
            newtenant.environmenturl.add(newenvironmenturl3)


            #first find out current homepage 
            currenthomepage  = HomePage.objects.first()
            #clear old homepages
            HomePage.objects.all().exclude(id=currenthomepage.id).delete()
            #then copy Homepage
            currenthomepage.tenantid.clear()
            currenthomepage.tenantid.add(defaulttenant)
            pageid = currenthomepage.id

            text = currenthomepage.intro
            texttranslated = asyncio.run(translate_text(text,'nl','de'))

            newhomepage = currenthomepage.copy(recursive=False, copy_revisions=False, keep_live=False, update_attrs={'slug': 'NewSlug'})
            newhomepage.intro = texttranslated
            newhomepage.save()
            newhomepage.tenantid.clear()
            newhomepage.tenantid.add(newtenant)
            self.stdout.write(self.style.SUCCESS('Created a new homepage'))


            self.stdout.write(self.style.SUCCESS('Successfully created sample data'))
