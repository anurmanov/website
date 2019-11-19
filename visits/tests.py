from django.test import TestCase
from medsmartcom.settings import SESSION_COOKIE_AGE, REDIS_KEY_PREFIX, REDIS_HOST, REDIS_PORT
import redis

class VisitsTest(TestCase):
    def setUp(self):
        pass
    def gatherVisitStatistics(self, key):
        client = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, db = 1)
        data = client.hgetall('medsmartcom:visits' + (':' + key if key else ''))
        d = {} # словарь обшей статистики
        dd = {} #  словарь детальной статистики
        for k in data:
            key = k.decode('utf-8')
            i = key.find(':')
            if i == -1:
                d[key] = data[k].decode('utf-8')
            else:
                fragments = key.split(':')
                internal_key = fragments[0]
                internal_value = key[i+1:]
                if not dd.get(internal_key, None):
                    dd[internal_key] = {}
                dd[internal_key][internal_value] = data[k].decode('utf-8')
        total_d = {}
        total_d['total'] = d
        total_d['details'] = dd
        return total_d
    def testVisitStatistics(self):
        d = self.gatherVisitStatistics(None)
        assert type(d) == dict
        assert d.get('total','error') != 'error'
        assert d['total'].get('total','error') != 'error'
        assert type(int(d['total']['total'])) == int
        assert d.get('details','error') != 'error'
        
