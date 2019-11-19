import re
import redis
import json
import random
import base64
from io import BytesIO
import psycopg2
from django.shortcuts import render, Http404, HttpResponse
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import ensure_csrf_cookie
from medsmartcom.settings import SESSION_COOKIE_AGE, REDIS_KEY_PREFIX, REDIS_HOST, REDIS_PORT
from medsmartcom.settings import GEOLITE_DB_NAME, GEOLITE_DB_HOST, GEOLITE_DB_PORT, GEOLITE_DB_USER, GEOLITE_DB_CONNECTION_OPTION
from visits.image import ImageCaptcha
from visits.tasks import save_captcha_text_to_cache, get_session_number, check_captcha, send_email

def visits_json_view(request):
    """This view-function responds on GET method with statistics information in JSON format
    
    key GET parameter contains required url page which user wanted to observe statistics.
    Statistics stored in redis-server.
    """ 
    if request.method == 'GET':
        if request.user.is_authenticated:
            key = request.GET.get('key','')
            client = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db = 1)
            data = client.hgetall(REDIS_KEY_PREFIX + ':visits' + (':' + key if key else ''))
            #dict for general statistics
            d = {}
            #for detail statistics
            dd = {}
            for k in data:
                key = k.decode('utf-8').replace('\"','')
                i = key.find(':')
                if i == -1:
                    d[key] = data[k].decode('utf-8')
                else:
                    internal_key = key[:i]
                    internal_value = key[i+1:]
                    if not dd.get(internal_key, None):
                        dd[internal_key] = {}
                    dd[internal_key][internal_value] = data[k].decode('utf-8').replace('\"','')
            total_d = {}
            total_d['total'] = d
            total_d['details'] = dd
            return JsonResponse(total_d)
        else:
            return HttpResponse(status = 401, content = '<h1>Unsufficient privileges for performing request!</h1>', charset = 'utf-8')
    else:
        return HttpResponseNotAllowed('<h1>Unsupported HTTP method!</h1>')

def country_iso_codes(request):
    """Responds with information about country name and its ISO codes. 
    
    Returns json-object containing information, which stored in PostgreSQL database.
    This endpoint could be used with country flag images for represent country 
    info on statistics page
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            conn = psycopg2.connect(host= GEOLITE_DB_HOST, port = GEOLITE_DB_PORT, 
            database=GEOLITE_DB_NAME, user=GEOLITE_DB_USER, 
            options = GEOLITE_DB_CONNECTION_OPTION)
            try:
                cur = conn.cursor()
                cur.execute('select lower(country_name), lower(country_iso_code) from country_locations_en')
                rows = cur.fetchall()
                response = {}
                for row in rows:
                    response[row[0].replace('\"','') if row[0] else row[0]] = row[1]
            finally:
                conn.close()
            return JsonResponse(response)
        else:
            return HttpResponse(status = 401, 
            content = '<h1>Unsufficient privileges for performing request!</h1>', charset = 'utf-8')
    else:
        return HttpResponseNotAllowed('<h1>Unsupported HTTP method!</h1>')

def statistic_pages(request):
    """Sends detailed statistics of visits of certain url"""
    if request.method == 'GET':
        if request.user.is_authenticated:
            key = request.GET.get('key','')
            client = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db = 1)
            keys = client.keys(REDIS_KEY_PREFIX + ':visits:*/')
            d = {}
            for k in keys:
                res = re.match(REDIS_KEY_PREFIX + ':visits:(\S*/)', k.decode('utf-8'))
                d[res.group(1)] = ''
            return JsonResponse(d)
        else:
            return HttpResponse(status = 401, content = '<h1>Unsufficient privileges for performing request!</h1>', charset = 'utf-8')
    else:
        return HttpResponseNotAllowed('<h1>Unsupported HTTP method!</h1>')


@ensure_csrf_cookie
def get_captcha(request):
    """Endpoint view-fucntion for generating captcha and checking captcha text
    
    Captcha image is generated via PIL module. View generates random text, 
    asynchronously save ro redis cache storage, generate image with this text 
    via image.py module based on PIL library, saves it to memory buffer then 
    convert buffer to base64encoded string representation.
    This string is sent to client like that - data:image/jpeg;base64,abd34....

    If request contains 'captcha' GET-param then view compares received text
    with captcha text stored in redis and responds to client with values
    'True' - if texts equal or 'False' - otherwise.
    """
    if request.method == 'GET':
        captcha_text = request.GET.get('captcha', None);
        session_number = get_session_number(request)
        if not captcha_text:
            captcha = ImageCaptcha(190, 60)
            symbols = list('QWERTYUOPASDFGHJKLZXCVBNM')
            text = ''.join([random.choice(symbols) for i in range(5)])
            if session_number:
                save_captcha_text_to_cache.apply_async(args=[text, session_number],
                retry = True,
                retry_policy =
                {'max_retries': 20,
                'interval_start': 0.01,
                'interval_step': 0.1,
                'interval_max': 3,})
            im = captcha.generate_image(text)
            buffer = BytesIO()
            im.save(buffer, format = 'JPEG')
            data = buffer.getvalue()
            return HttpResponse(status = 201, content='data:image/jpeg;base64,' + base64.b64encode(data).decode('utf-8'));
        else:
            return HttpResponse(status = 201, content=str(check_captcha(captcha_text, session_number)))#JsonResponse(int(check_captcha(captcha_text, session_number)), safe=False);
    else:
        return HttpResponseNotAllowed('<h1>Unsupported HTTP method!</h1>')

def feedback(request):
    """View-function for sending emails to vendors via celery task
    
    Return '1' or '0' if sending succeded.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'));
            session_number = get_session_number(request)
            if not check_captcha(data['captcha'], session_number):
                return JsonResponse('Incorrect captcha code!', safe = False)
            send_email.apply_async(args = [data],
            retry = True,
            retry_policy =
            {'max_retries': 20,
            'interval_start': 0.01,
            'interval_step': 0.3,
            'interval_max': 6,})
            return HttpResponse(status = 201, content='1')
        except json.JSONDecodeError as jex:
            #JsonResponse('Incorrect message format: '+request.body.decode('utf-8'), safe = False)
            return HttpResponse(status = 500, content='0') 
    else:
        return HttpResponseNotAllowed('<h1>Unsupported HTTP method!</h1>')

class VisitStatisticsView(LoginRequiredMixin, TemplateView):
    """View-class for representation statistics on template visits.html
    
    visits.html page uses visits.css and visits.js
    """
    template_name = 'visits.html'  
    def get(self, request, *args, **kwargs):
        return super(VisitStatisticsView, self).get(request, *args, **kwargs)

    
    
