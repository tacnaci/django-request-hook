import json, requests
from threading import Thread
from django.utils import timezone
from django.conf import settings

class LogTracker:

    __request_hook_excludes = getattr(settings, 'REQUEST_HOOK_EXCLUDES', [])
    __request_hook_url = getattr(settings, 'REQUEST_HOOK_LOG_URL', '')
    __request_hook_token = getattr(settings, 'REQUEST_HOOK_LOG_TOKEN', '')

    def __init__(self, get_response):
        self.get_response = get_response

        self.data = {}

    def _send_log(self):
        response = requests.post(self.__request_hook_url, 
                                 auth=(self.__request_hook_token, ''), 
                                 json=self.data, verify=False)
        return response.status_code

    def __call__(self, request):
        start_time = timezone.now()

        request_content = request.body.decode()
        try:
            request_content = json.loads(request_content)
        except:
            request_content = request.POST.dict()

        response = self.get_response(request)
        
        response_content = response.content.decode()
        try:
            response_content = json.loads(response_content)
        except:
            pass

        end_time = timezone.now()
        duration = (end_time - start_time).microseconds

        if request.path in self.__request_hook_excludes:
            return response

        self.data={
            'time': start_time.__str__(),
            'headers': dict(request.headers),
            'user': request.user.username if request.user.is_authenticated else None,
            'content': request_content,
            'method': request.method,
            'scheme': request.scheme,
            'path': request.path,
            'query_params': request.GET.dict(),
            'response_headers': dict(response.headers),
            'status_code': response.status_code,
            'response_content': response_content,
            'duration': duration  
        }
        Thread(target=self._send_log).start()

        return response
    
