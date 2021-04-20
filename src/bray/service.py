from bray import config, etl, geoclient, logger


# FIXME global variable, not thread-safe
class Registry:
    def __init__(self, settings_override=None, registry_override=None):
        logger.info("Initializing Registry with settings %s and registry %s", settings_override, registry_override)
        if settings_override is None:
            settings_override = config.settings
        self.settings = settings_override

        if registry_override is None:
            registry_override = {}
        self.registry = registry_override

        logger.debug("Registry initialized with settings %s and registry %s", self.settings, self.registry)
        # FIXME this is fugly
        geoclient.register_services(self.settings, self.registry)
        etl.register_services(self.settings, self.registry)

    def get_job(self):
        return self.registry[etl.JOB_ID]
