from keystoneclient import client

from .settings import from_settings

def request_keystone(request):
    return Keystone(request)

class Keystone(object):
    user_id = None
    username = None

    def __init__(self, request):
        self.request = request
        self.settings = from_settings(request.registry.settings)
        self.settings = { k: v for (k, v) in self.settings.items() if v }


