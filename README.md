# bidding-software
Django Bidding Software for LSU Christian Union Promise Auction.

# Set-up on local
- Ensure `DEBUG = True` in settings.py.
- Run `pip install virtualenv`.
- Run `bidding-software % virtualenv -p *PYTHON LOCATION* venv`, where python location is the result of `which python3`.
- Enter the virtual environment using `source venv/bin/activate`.
- Run `pip install django` in the venv.
- Run `pip install django-import-export` in the venv.
- Run `brew install postgresql` in the venv.
- Run `pip install psycopg2-binary` in the venv.
- Run `python manage.py createsuperuser` in venv and enter a username/email/password.
- Run `python manage.py runserver 0.0.0.0:8000` in the venv.
- Open `http://0.0.0.0:8000/` in a browser.

# Set-up on live

# How to use the software
- Navigate to the /admin URL (e.g. `http://0.0.0.0:8000/admin` on local) and log in with your superuser account to add items to bid on.
- Navigate to the base URL (e.g. `http://0.0.0.0:8000/` on local) to log in as a user and bid on promises.

# MISC USEFUL COMMANDS

sudo systemctl daemon-reload
sudo systemctl restart gunicorn <—— use this one when code changes
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
sudo systemctl status gunicorn

sudo nano /etc/systemd/system/gunicorn.socket
sudo nano /etc/systemd/system/gunicorn.service

Restart nginx: sudo nginx -t && sudo systemctl restart nginx
