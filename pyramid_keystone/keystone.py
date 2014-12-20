import logging
log = logging.getLogger(__name__)

from keystoneclient import session as kc_session
from keystoneclient.auth.identity import v3 as kc_v3

from keystoneclient.openstack.common.apiclient import exceptions as kc_exceptions

from .settings import from_settings

def request_keystone(request):
    return Keystone(request)

class Keystone(object):
    user_id = None
    username = None
    _authed = False
    _session = None

    def __init__(self, request):
        self.request = request
        self.settings = from_settings(request.registry.settings)
        self.settings = { k: v for (k, v) in self.settings.items() if v }

    def _get_unscoped_session(self, token=None, username=None, password=None):
        try:
            auth_password = kc_v3.PasswordMethod(
                    user_domain_name=self.settings['user_domain_name'],
                    username=username,
                    password=password
                    )

            auth_token = kc_v3.TokenMethod(
                    token=token
                    )

            auth_methods = []

            if token is not None:
                auth_methods.append(auth_token)

            if username is not None and password is not None:
                auth_methods.append(auth_password)

            auth = kc_v3.Auth(auth_url=self.settings['auth_url'], auth_methods=auth_methods)

            sess = kc_session.Session(auth=auth)

            log.debug('Fetching unscoped token')
            unscoped_token = sess.get_token()
            log.debug('Fetched unscoped token: {}'.format(unscoped_token))

            if unscoped_token:
                self._authed = True
                self._session = sess
                self.request.session['keystone_token'] = unscoped_token
            else:
                if 'keystone_token' in self.request.session:
                    del self.request.session['keystone_token']
        except (kc_exceptions.Unauthorized, kc_exceptions.AuthorizationFailure) as e:
            return

