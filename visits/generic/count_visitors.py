from decorator import decorator
import django_redis
from django.http import HttpRequest, HttpResponse
from visits.tasks import increment_visit_counter, get_session_number

social_media_sources = ['instagram', 'facebook', 'twitter']

@decorator
def count_visitors(func, *args, **kwargs):
    """
    start celery task.
    connect to redis.
    check session
    ++counter
    """
    if isinstance(args[1], HttpRequest):
        request = args[1]
        ip_addr = request.META.get('HTTP_X_FORWARDED_FOR', '')
        social_media = None
        if request.method == 'GET':
            social_media = request.GET.get('s','').lower()
            if social_media and social_media not in social_media_sources:
                return HttpResponse(status = 400, reason = 'The request has incorrect syntax!') 
        session_number = get_session_number(request)
        increment_visit_counter.apply_async(args=[ip_addr, session_number, request.path, social_media],
        retry = True,
        retry_policy =
        {'max_retries': 20,
        'interval_start': 0.01,
        'interval_step': 0.1,
        'interval_max': 3,})

    result = func(*args, **kwargs)
    return result
