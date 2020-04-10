# flask-webhook
web hook server on Flask which receives POST request

# Prerequisite server environment

```bash
sudo apt install python3-pip
sudo apt install gunicorn
sudo apt install git
sudo apt-get install python3-venv
cd ~
git clone https://github.com/yukilab2/flask-webhook.git

cd flask-webhook
python3 -m venv venv
source ./venv/bin/activate
(venv) pip install -r requirements.txt

# gunicorn and venv setup test
(venv) gunicorn --bind '0.0.0.0:<server_port>' --env FLASK_POST_KEY=<flask_post_key> --chdir <work_directory> --user <user> --group <group> -w 1 hook.main:app


# environment variable FLASK_POST_KEY shall be set properly
# (following your server config,) nginx, gunicorn shall be setup to call hook/main.py at appropriate directory
```