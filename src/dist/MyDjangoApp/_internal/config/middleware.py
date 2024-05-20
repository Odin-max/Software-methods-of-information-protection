from django.utils.deprecation import MiddlewareMixin
from users.models import User

class CustomUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'user_id' in request.session:
            try:
                request.user = User.objects.get(id=request.session['user_id'])
            except User.DoesNotExist:
                request.user = None
        else:
            request.user = None