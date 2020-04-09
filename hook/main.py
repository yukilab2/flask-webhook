from flask import Flask, request, render_template
import os
import subprocess
import shlex

app = Flask(__name__)


def kicked():
    command = 'git pull'
    args = shlex.split(command)
    subprocess.call(args, shell=True)


@app.route('/post', methods=['POST'])
def process_post():
    error = None
    if request.method == 'POST':
        if 'secret' in request.form.keys() and request.form['secret'] == os.environ['FLASK_POST_KEY']:
            kicked()
        else:
            error = 'Invalid secret'
    return render_template('index.html', error=error)
