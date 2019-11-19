import binascii
import uuid
from datetime import datetime
import redis
import psycopg2
from django.http import HttpRequest
from django.core.mail import send_mail
from medsmartcom.celery import app
from medsmartcom.settings import SESSION_COOKIE_AGE, REDIS_KEY_PREFIX, REDIS_HOST, REDIS_PORT, EMAIL_HOST_USER
from medsmartcom.settings import GEOLITE_DB_NAME, GEOLITE_DB_HOST, GEOLITE_DB_PORT, GEOLITE_DB_USER, GEOLITE_DB_CONNECTION_OPTION

def get_session_number(request):
    """Function for getting session number. Generaly used in views"""
    if isinstance(request, HttpRequest):
        session_number = request.session.session_key
        if not session_number:
            request.session.create()
            session_number = request.session.session_key
        return session_number
    return None

def check_captcha(captcha_text, session_number):
    """Function connects to redis, compares captcha text with value from sessional redis key"""
    client = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db = 1)
    session_key = REDIS_KEY_PREFIX.encode('utf-8') + b':sessions:' + session_number.encode('utf-8')
    captcha = client.hget(session_key, 'captcha');
    return captcha.decode('utf-8').strip() == captcha_text.strip().lower()

def find_location(ip_addr):
    """Function for getting country and city via ip_addr param.
    
    PostgreSQL database geolite_max_mind2 stores info about ip-addresses 
    from public database Geolite_max_mind's company.
    """
    try:
        conn = psycopg2.connect(host=GEOLITE_DB_HOST, port = GEOLITE_DB_PORT, database=GEOLITE_DB_NAME, user=GEOLITE_DB_USER, options = GEOLITE_DB_CONNECTION_OPTION)
        location = 'unknown:unknown' 
        try:
            cur = conn.cursor()
            cur.execute('select find_location(\'' + ip_addr + '\');' )
            row = cur.fetchone()
            location = row[0]
        finally:
            conn.close()
    except Exception:
        location = 'error:error'
    return location

def build_message(msg_details):
    """Function for arranging message for sending by email"""
    msg = """
Добрый день!

Посетитель сайта medicalsmartcompany отправил Вам сообщение.
Детали сообщения:

"""
    for key in filter(lambda key: key!='captcha', msg_details.keys()):
        msg += key + ': ' + ('\n' if key == 'message' else '') + msg_details[key] + '\n'

    return msg


@app.task(bind = True, expires = 60, acks_late = True)
def send_email(self, msg_details):
    """Celery task for sending email via function send_mail"""
    msg = build_message(msg_details)
    send_mail('medicalsmartcompany.com', msg, EMAIL_HOST_USER, ['feedback.msc@mail.ru'], fail_silently = True);

@app.task(bind = True, expires = 60, acks_late = True)
def save_captcha_text_to_cache(self, text, session_number):
    """Celery task for saving captcha text in session key of redis server"""
    try:
        client = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db = 1)
        session_key = REDIS_KEY_PREFIX.encode('utf-8') + b':sessions:' + session_number.encode('utf-8')
        client.hset(session_key, 'captcha', text.lower());
    except:
        self.retry()    

@app.task(bind = True, expires = 60, acks_late = True)
def remove_redis_key(self, key):
    """Celery task for removing key from redis server"""
    try:
        client = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db = 1)
        redis_key = REDIS_KEY_PREFIX.encode('utf-8') + b':visits:' + key.encode('utf-8')
        client.delete(redis_key);
    except:
        self.retry()    


@app.task(bind = True, expires = 60, acks_late = True)
def increment_visit_counter(self, ip_addr, session_number, request_path, social_media):
    """Celery task for added visit to structured statistics of redis server
    
    Algorithm gather statistics grouped by country, city, year, month.
    For better performance redis commands are executed in pipiline.
    """
    try:
        client = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db = 1)
        now = datetime.today()
        year = str(now.year)
        month = str('' if now.month > 9  else '0') + str(now.month)
        day = str('' if now.day > 9 else '0') + str(now.day)
        hour = str('' if now.hour > 9 else '0') + str(now.hour)
        minute = str('' if now.minute > 9 else '0') + str(now.minute)
        session_key = REDIS_KEY_PREFIX.encode('utf-8') + b':sessions:' + session_number.encode('utf-8')
        counter_key = REDIS_KEY_PREFIX.encode('utf-8') + b':visits:' + request_path.encode('utf-8')
        pipeline = client.pipeline()
        new_session = False
        new_visit_on_page = False
        if client.exists(session_key) == 0:
            location = find_location(ip_addr).lower()
            country, city = location.split(':')
            pipeline.hincrby(REDIS_KEY_PREFIX.encode('utf-8') + b':visits', b'total', 1) # total counter
            if social_media:
                pipeline.hincrby(REDIS_KEY_PREFIX.encode('utf-8') + b':visits', social_media.encode('utf-8'), 1) # social media counter
            pipeline.hincrby(REDIS_KEY_PREFIX.encode('utf-8') + b':visits', b'country:' + country.encode('utf-8'), 1) # total counter
            pipeline.hincrby(REDIS_KEY_PREFIX.encode('utf-8') + b':visits', b'country_city:' + location.encode('utf-8'), 1) # total counter
            pipeline.hset(session_key, counter_key, 1) # page counter during current session
            if social_media:
                pipeline.hset(session_key, social_media.encode('utf-8'), 1) # social media counter
            pipeline.hset(session_key, b'country', country.encode('utf-8')) # set country in current session
            pipeline.hset(session_key, b'city', city.encode('utf-8')) #  set city in current session
            pipeline.hset(session_key, b'start time', year.encode('utf-8') + b':' + month.encode('utf-8') + b':' + day.encode('utf-8') + b':' + hour.encode('utf-8') + b':' + minute.encode('utf-8')) #  set city in current session
            new_session = True
            new_visit_on_page = True    
        else:
            if client.hexists(session_key, counter_key) == 0:
                new_visit_on_page = True   
            pipeline.hincrby(session_key, counter_key, 1) # page counter during current session
            country = client.hget(session_key, b'country').decode('utf-8')
            city = client.hget(session_key, b'city').decode('utf-8')
            location = country + ':' + city
        pipeline.expire(session_key, SESSION_COOKIE_AGE) 
        if new_session or new_visit_on_page: 
            pipeline.hincrby(counter_key, b'total', 1) # page counter
            if social_media:
                pipeline.hincrby(counter_key, social_media.encode('utf-8'), 1) # social media counter
            pipeline.hincrby(counter_key, b'country:' + country.encode('utf-8'), 1) # page counter
            pipeline.hincrby(counter_key, b'country_city:' + location.encode('utf-8'), 1) # page counter
            pipeline.hincrby(counter_key, b'year:' + year.encode('utf-8'), 1) # page counter via year
            pipeline.hincrby(counter_key, b'year_month:' + year.encode('utf-8') + b':' + month.encode('utf-8'), 1) # page counter via monthes
            pipeline.hincrby(counter_key, b'year_country:' + year.encode('utf-8') + b':' + country.encode('utf-8'), 1) # page counter via year
            pipeline.hincrby(counter_key, b'year_month_country_city:' + year.encode('utf-8') + b':' + month.encode('utf-8') + b':' + country.encode('utf-8') + b':' + city.encode('utf-8'), 1) # page counter via monthes
            #redis stores statictics of visits of last month days by days
            temp_key = counter_key + b':byday:' + year.encode('utf-8') + b':' + month.encode('utf-8') + b':' + day.encode('utf-8')
            pipeline.incrby(temp_key, 1) # page counter via days
            pipeline.expire(temp_key, 2678400) # store key 31 days
            #redis stores statictics of visits of last day by hours
            temp_key = counter_key + b':byhour:' + hour.encode('utf-8')
            pipeline.incrby(temp_key, 1) # page counter via hours
            pipeline.expire(temp_key, 86400) # store key 24 hours
        pipeline.execute()
    except:
        self.retry()    