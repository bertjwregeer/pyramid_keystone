
default_settings = [
        ('auth_url', str, 'http://localhost:5000/v3'),
        ('region', str, 'RegionOne'),
        ('user_domain_name', str, 'Default'),
        ('cacert', str, ''),
]

def parse_settings(settings):
    parsed = {}

    def populate(name, convert, default):
        sname = '%s%s' % ('keystone.', name)
        value = convert(settings.get(sname, default))
        parsed[sname] = value

    for name, convert, default in default_settings:
        populate(name, convert, default)

    return parsed

def includeme(config):
    """ Set up standard configurator registrations.  Use via:

    .. code-block:: python

       config = Configurator()
       config.include('pyramid_keystone')

    """

    # We use an action so that the user can include us, and then add the
    # required variables, upon commit we will pick up those changes.
    def register():
        registry = config.registry
        settings = parse_settings(registry.settings)

        registry.settings.update(settings)

    config.action('keystone-configure', register)

    # Allow the user to use our auth policy (recommended)
    config.add_directive('keystone_auth_policy', '.authentication.add_auth_policy')

    # Add the keystone property to the request
    config.add_request_method('.keystone.request_keystone', name='keystone', property=True, reify=True)

