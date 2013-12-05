# -*- coding: utf-8 -*-

import urllib
import urllib2
import json
import logging
from datetime import datetime

API_URL = 'https://es.wikipedia.org/w/api.php'

logging.basicConfig(
    format='%(levelname)s %(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO,
)

def get_data():
    stop = False
    to_save = []
    data = {
        'action': 'query',
        'list': 'embeddedin',
        'eititle': 'Plantilla:Coord',
        'eilimit': 500,
        'einamespace': 0,
        'format': 'json',
    }
    while not stop:
        req = urllib2.Request(API_URL, urllib.urlencode(data))
        response = urllib2.urlopen(req)
        contents = json.load(response)
        results = contents['query']['embeddedin']
        logging.info('Obtenidos %s resultados (total: %s)' % (len(results), len(to_save)))
        to_save += results
        if 'query-continue' in contents.keys():
            data['eicontinue'] = contents['query-continue']['embeddedin']['eicontinue']
        else:
            stop = True
    filename = 'results.json'
    logging.info('Escribiendo resultados en %s' % filename)
    f = open(filename, 'w')
    f.write(json.dumps(to_save))
    f.close()

def main():
    get_data()

if __name__ == '__main__':
    main()
