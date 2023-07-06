# Django Request Hook

Django middlewares to track request/response logs. Catch the logs and send it to anywhere you want through HTTP.

## Installation

You can install the Django Request Hook from [PyPI](https://pypi.org/project/django-request-hook/)

## How to use

1. PyPI

```
pip install django-request-hook
```

2. Add in MIDDLEWARE

```
MIDDLEWARE = [
    ...,
    'django_request_hook.middleware.LogTracker'
]
```

3. Settings

```
REQUEST_HOOK_EXCLUDES = []

REQUEST_HOOK_LOG_URL = 'https://xxx/api/log'

REQUEST_HOOK_LOG_TOKEN = 'mytoken'
```
