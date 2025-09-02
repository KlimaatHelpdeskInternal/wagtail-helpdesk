from wagtail_helpdesk.tenants.models import Tenant, EnvironmentURL
from wagtail_helpdesk.cms.models import HomePage
from django.core.exceptions import ValidationError

def add_new_tenant(app, template_id, newtenant_id, templateName, templateDescription):

        #first check if the template tenant exists
        templatetenant = Tenant.objects.get(id=template_id)
        if templatetenant is None:
                message = 'Template tenant not found! id "%s"' % template_id
                raise ValidationError(message)
        # check if new 
        newtenants = Tenant.objects.filter(id=newtenant_id)
        if len(newtenants)>0:
                newtenant  = newtenants[0]
                #newtenant already exists
                #remove answers 
                #answers = Answer.objects.get(tenantid = newtenant_id)
                #for tmpanswer in answers:
                        #tmpanswer.delete()

                #remove environments 
                environmenturls = EnvironmentURL.objects.filter(tenant = newtenant)
                if (environmenturls.exists() and len(environmenturls)>0):
                        for tmpenvironmenturl in environmenturls:
                                tmpenvironmenturl.delete()

                #remove environments 
                homepages = HomePage.objects.filter(tenantid = newtenant)
                for tmphomepage in homepages:
                        pass



                #remove tenant
                newtenant.delete()
                app.stdout.write(
                        app.style.SUCCESS('Removed tenant with tenant id "%s"' % newtenant_id))
        
        #add the new tenant
        newtenant = Tenant(id=newtenant_id, name = templateName, description = templateDescription)
        newtenant.save()
        app.stdout.write(
            app.style.SUCCESS('Successfully created a new tenant based on tenant id "%s"' % template_id))

        return newtenant

