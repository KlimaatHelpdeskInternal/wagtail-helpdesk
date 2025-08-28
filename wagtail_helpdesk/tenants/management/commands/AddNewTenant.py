from django.core.management.base import BaseCommand, CommandError

from wagtail_helpdesk.tenants.models import Tenant
from django.core.exceptions import ValidationError



class Command(BaseCommand):
    help = "Creates a new based on a template tenant"

    def add_arguments(self, parser):
        parser.add_argument("template_id", type=int)
    
    def handle(self, *args, **options):
            template_id = options["template_id"]

            #first check if the template tenant exists
            templatetenant = Tenant.objects.get(id=template_id)
            if templatetenant is None:
                  message = 'Template tenant not found! id "%s"' % template_id
                  raise ValidationError(message)
            #then 

            self.stdout.write(
                self.style.SUCCESS('Successfully created a new tenant based on tenant id "%s"' % template_id)
            )
