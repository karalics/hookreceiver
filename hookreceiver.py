# -*- coding: utf-8 -*-
''' main application file of hookreceiver. '''
import subprocess
import hashlib
import hmac
import config
from flask import Flask
from flask import request


application = Flask(__name__)
# For local tests: curl -i -X POST -H 'Content-Type: application/json' -d \
# '{"name": "New item", "year": "2009"}' http://localhost:8000


@application.route('/', methods=['GET', 'POST'])
def index():
    ''' Main Index Function'''
    if request.method == 'GET':
        return 'OK'
    elif request.method == 'POST':
        content = request.data
        app_key = bytes(config.APP_KEY, 'utf-8')
        hmac_hash = hmac.new(app_key, content, hashlib.sha1).hexdigest()
        signature = 'sha1=' + hmac_hash
        if (
            signature == request.headers.get('X-Hub-Signature') or
            request.headers.get('X-Gitlab-Token') == config.APP_KEY
        ):
            subprocess.Popen(
                '/bin/bash {0}/deploy.sh'.format(config.PROJECT_PATH))
            return 'OK\n'
        else:
            return 'ERROR\n'

if __name__ == "__main__":
    application.run(host='0.0.0.0')
