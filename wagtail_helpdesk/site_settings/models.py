from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from django.utils.translation import gettext_lazy as _
from wagtail.models import Site
# Create your models here.
@register_setting
class SiteSettings(BaseSiteSetting ):
    id = models.AutoField(_("id"), primary_key=True)
    name = models.CharField(_("name"), max_length=50)
    css_file_name = models.CharField(_("name"), max_length=50, default="main.css")

    sitename = models.CharField(_("sitename"), max_length=50, null=True)

    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_(
            "This is the logo used for display this site"
        ),
    )
    logo_on_black = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_(
            "This is the logo used for this site on black background "
        ),
    )
    logofooter = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_(
            "This is the logo used in the footer for display this site"
        ),
    )

    favicon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_(
            "This is the favicon used for display this site"
        ),
    )
    apple_touch_icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_(
            "This is the png icon used for apple devices for this site"
        ),
    )
    android_chrome_icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_(
            "This is the png icon used for android devices for this site"
        ),
    )
    #scss_file = models.ForeignKey(
    #    "wagtailimages.Image",
    #    null=True,
    #    blank=True,
    #    on_delete=models.SET_NULL,
    #    related_name="+",
    #    help_text=_(
    #        "This is the scss file for this site"
    #    ),
    #)