
def parse_options_from_settings(settings, settings_prefix):
    """ Parse options for use with Keystone """
    def sget(name, default=None):
        return settings.get(settings_prefix + name, default)
   
def setup_keystone(config, settings_prefix='keystone.'):
    """ Register a function that does the keystone setup

    This function is available on the Pyramid configurator after
    including the package:

    .. code-block:: python

       config.setup_keystone(settings_prefix='keystone.')

    By default this will attempt to setup keystone using the
    settings_prefix='keystone.', when called again with a different name, will
    override previous setup
    """

    def register():
        registry = config.registry
        opts = parse_options_from_settings(
            registry.settings, settings_prefix)

    config.action(('keystone-configure', extension), register)

def includeme(config):
    """ Set up standard configurator registrations.  Use via:

    .. code-block:: python

       config = Configurator()
       config.include('pyramid_keystone')
    
    """
    config.add_directive('setup_keystone', setup_keystone)

