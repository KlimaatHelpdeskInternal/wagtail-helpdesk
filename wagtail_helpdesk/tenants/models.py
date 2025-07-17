
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class EnvironmentURL(models.Model):
    id = models.IntegerField(_("id"), primary_key=True, default= 0)
    name = models.CharField(_("name"), max_length=50)
    urlroot = models.URLField(
        _("urlroot"), max_length=255, blank=False, null=True
    )
    def __str__(self):
        return self.name



@register_snippet
class Tenant(models.Model):
    id = models.IntegerField(_("id"), primary_key=True, default= 0)
    name = models.CharField(_("name"), max_length=50)
    environmenturl = models.ManyToManyField(EnvironmentURL,verbose_name="list of environment URL's")
    description = models.CharField(
        _("description"), max_length=255, blank=False, null=True
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("environmenturl"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")
        ordering = ["id"]

    def __str__(self):
        return self.name

    def get_prefiltered_search_params(self):
        return "?{}=".format(self.name)


