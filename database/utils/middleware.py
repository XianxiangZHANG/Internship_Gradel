from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 1.Access processing without logging in
        if request.path_info in ["/login/", "/img/code/"]:
            return

        # 2.Get session
        info_dict = request.session.get("info")

        # Not logged in
        if not info_dict:
            return redirect('/login/')

        # Has logged
        request.info_dict = info_dict
