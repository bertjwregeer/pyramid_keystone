
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

