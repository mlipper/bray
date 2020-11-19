from bray import config
from bray import etl
from bray import geoclient


# FIXME global variable, not thread-safe
class Registry:
    def __init__(self, settings_override=None, registry_override=None):

        if settings_override is None:
            settings_override = config.settings
        self.settings = config.settings

        if registry_override is None:
            registry_override = {}
        self.registry = registry_override

        # FIXME this is fugly
        geoclient.register_services(self.settings, self.registry)
        etl.register_services(self.settings, self.registry)

    def get_job(self):
        return self.registry[etl.JOB_ID]
