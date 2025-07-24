from django.apps import AppConfig
from logging import getLogger

from apps.core.utils import check_for_debug_settings_in_production


class CoreConfig(AppConfig):
    name = "apps.core"

    def ready(self):
        logger = getLogger(__name__)
        logger.debug("testmesage")
        check_for_debug_settings_in_production()
