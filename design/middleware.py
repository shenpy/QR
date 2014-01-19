import datetime
from django.core.cache import cache
from django.core.urlresolvers import resolve
from django.conf import settings

class OnlineUserMiddleware:
    def process_request(self, request):
        current_user = request.user
        if current_user.is_authenticated() and \
                resolve(request.path).url_name != \
                    u'django.contrib.staticfiles.views.serve':
            now = datetime.datetime.now()
            cache.set('active_%s'% (current_user.username), now,
                                    settings.USER_ACTIVE_TIMEOUT)
