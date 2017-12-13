# hookreceiver

A simple flask script that helps to receive and handle webhooks sent from github or gitlab. 

disclaimer: Use at your own risk! 

## an example of usage
(with flask, gunicorn, nginx and bash)

ex: receive webhook, perform automatic git pull on your server.
```
git clone git@github.com:karalics/hookreceiver
cd hookreceiver
# Works with python 3 only
pyvenv-3.4 .
source bin/activate
pip insstall -r requirements.txt
chmod 600 config.py
cp example_deploy.sh /your/local/repository/deploy.sh
```
Edit your config.py file. (path to your local repository and your github or gitlab webhook secret)

## Optional systemd script to create a daemon

alternatively you can start the hookreceiver in foreground:
`gunicorn -b 127.0.0.1:8008 hookreceiver`

Create a new file hookreceiver.service in /etc/systemd/system 

```
#file: /etc/systemd/system/hookreceiver.service
# change "user" to your username
[Unit]
Description=todamoon hookreceiver
After=network.target multi-user.target

[Service]
User=user
Environment="PYTHONPATH=/home/user/hookreceiver/bin/python"
WorkingDirectory=/home/user/hookreceiver
ExecStart=/home/user/hookreceiver/bin/gunicorn -b 127.0.0.1:8008 -w 2 --log-file /home/user/hookreceiver/hookreceiver.log hookreceiver

[Install]
WantedBy=multi-user.target
```
Finish systemd configuration:
```
sudo systemctl daemon-reload
sudo systemctl start hookreceiver
sudo systemctl enable hookreceiver
```
Edit nginx configuration in your nginx domain config file ex: /etc/nginx/yourdomain.conf

```
...
location =  /hookreceiver/ {
        proxy_pass          http://localhost:8008/;
    }

...
```

test it: `curl http://yourdomain.com/hookreceiver` should return "OK" in your browser. Now you can add a webhook on github or gitlab that points to yourdomain.com/hookreceiver


