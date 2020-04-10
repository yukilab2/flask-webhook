from flask import Flask, request, render_template
import os
import json
import subprocess
import shlex
import hmac, hashlib

app = Flask(__name__)


@app.route('/post', methods=['POST'])
def process_post():
    error = None
    if request.method == 'POST':
        # https://developer.github.com/webhooks/securing/
        payload = request.data
        secret = os.environ['FLASK_POST_KEY']
        m = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha1)
        recalculated_signature = 'sha1=' + m.hexdigest()
        github_signature = request.headers.environ["HTTP_X_HUB_SIGNATURE"]
        t = hmac.compare_digest(recalculated_signature, github_signature)
        try:
            data = json.loads(payload.decode())
            events = data['hook']['events']
            if 'push' not in events:
                error = 'this is not a push event: ' + str(events)
        except Exception as e:
            error = 'bad json format: ' + str(e) + ' ' + payload.decode()
        if not error:
            if t:
                try:
                    command = './post_command.sh'
                    args = shlex.split(command)
                    home = os.environ['HOME']
                    with open( home + '/service.log', 'a') as fd:
                        error = subprocess.check_output(args, stderr=subprocess.STDOUT).decode()
                        fd.write(error)
                except Exception as e:
                    return str(e) + ': ' + (error if error else '')
            else:
                error = 'Invalid signature'
    return render_template('index.html', error=error)
