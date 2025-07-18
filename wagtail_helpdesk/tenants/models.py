
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
    favicon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_(
            "This is the favicon used for display the tenant"
        ),
    )
    apple_touch_icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_(
            "This is the png icon used for apple devices for this tenant"
        ),
    )
    android_chrome_icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_(
            "This is the png icon used for android devices for this tenant"
        ),
    )
    scss_file = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_(
            "This is the scss file for this tenant"
        ),
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("environmenturl"),
        FieldPanel("description"),
        FieldPanel("favicon", help_text=_("Image to be used as favicon")),
        FieldPanel("apple_touch_icon", help_text=_("Image to be used as apple_touch_icon")),
        FieldPanel("android_chrome_icon", help_text=_("Image to be used as android_chrome_icon")),
        FieldPanel("scss_file", help_text=_("CSS file to be used as scss_file")),

    ]

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")
        ordering = ["id"]

    def __str__(self):
        return self.name

    def get_prefiltered_search_params(self):
        return "?{}=".format(self.name)


