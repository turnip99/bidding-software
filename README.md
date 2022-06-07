# bidding-software
Django Bidding Software for online auctions/promise auctions. Originally built for LSU Christian Union's annual promise auction.

# Set-up on local
- Ensure `DEBUG = True` in settings.py.
- Run `pip install virtualenv`.
- Run `bidding-software % virtualenv -p *PYTHON LOCATION* venv`, where python location is the result of `which python3`.
- Add the exporting of environment variables to the bottom of `venv/bin/activate` by pasting in:
```
export DEBUG="True"
export DJANGO_SECRET_KEY="foo"
export DJANGO_ALLOWED_HOSTS="127.0.0.1,0.0.0.0,localhost"
```
- Enter the virtual environment using `source venv/bin/activate`.
- Run `pip install django` in the venv.
- Run `brew install postgresql` in the venv.
- Run `pip install gunicorn psycopg2-binary dj-database-url django-import-export django-cors-headers` in the venv.
- Run `python manage.py createsuperuser` in venv and enter a username/email/password.
- Run `python manage.py runserver 0.0.0.0:8000` in the venv.
- Open `localhost:8000` in a browser.
- Hit `CTRL+C` to exit the server.
- Run `pip freeze > requirements.txt` to ensure that the requirements file is up to date.
- Type `deactivate` to leave venv.

# Set-up on live
- Follow the second half of this tutorial to set up a app on DigitalOcean (or other cloud provider of choice). https://docs.digitalocean.com/tutorials/app-deploy-django-app/

# How to use the software
- Navigate to the /admin URL (e.g. `http://0.0.0.0:8000/admin` on local) and log in with your superuser account to add items to bid on.
- Navigate to the base URL (e.g. `http://0.0.0.0:8000/` on local) to log in as a user and bid on promises.