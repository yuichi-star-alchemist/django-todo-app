from django.conf import settings

class SessionCookieNameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # admin用のクッキー名に切り替え
        if request.path.startswith('/admin/'):
            settings.SESSION_COOKIE_NAME = 'admin_sessionid'
            settings.AUTH_USER_MODEL = 'App.AdminSiteUsers'
        # アプリ用のクッキー名に切り替え
        else:
            settings.SESSION_COOKIE_NAME = 'app_sessionid'
            settings.AUTH_USER_MODEL = 'App.AppUsers'

        response = self.get_response(request)
        return response