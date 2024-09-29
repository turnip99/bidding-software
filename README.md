# bidding-software
Django Bidding Software for online auctions/promise auctions. Originally built for LSU Christian Union's annual promise auction.

# Set-up on local
- Install git, python, pip and brew.
- Clone this repository.
- Navigate to the root directory of the project in the terminal (Mac) or PowerShell (Windows).
- Run `pip install virtualenv`.
- Run `virtualenv venv`, where python location is the location of your python executable.
- MAC ONLY: Add the exporting of environment variables to the bottom of `venv/bin/activate` by pasting in:
```
export DEBUG="True"
export DJANGO_SECRET_KEY="foo"
export DJANGO_ALLOWED_HOSTS="127.0.0.1,0.0.0.0,localhost"
```
- WINDOWS ONLY: Add the exporting of environment variables to the bottom of `venv/Scripts/activate.ps1` by pasting in:
```
[System.Environment]::SetEnvironmentVariable("DEBUG", "True")
[System.Environment]::SetEnvironmentVariable("DJANGO_SECRET_KEY", "foo")
[System.Environment]::SetEnvironmentVariable("DJANGO_ALLOWED_HOSTS", "127.0.0.1,0.0.0.0,localhost")
```
- Enter the virtual environment using `source venv/bin/activate` (Mac) or `venv/Scripts/activate.ps1` (Windows).
- Run `pip install django` in the venv.
- Run `pip install -r requirements.txt` in the venv.
- Run `python manage.py migrate` in the env.
- Run `python manage.py createsuperuser` in the venv and enter a username/email/password.
- Run `python manage.py runserver 0.0.0.0:8000` in the venv.
- Open `localhost:8000` in a browser.
- Hit `CTRL+C` to exit the server.
- Type `deactivate` to leave venv.

# Set-up on live
- Follow steps 4 and 5 of of the following tutorial to set up a app on DigitalOcean. https://docs.digitalocean.com/tutorials/app-deploy-django-app/
- If you follow the above guide, you may encounter issues in step 5 while setting static files. If this is the case, you can upload the DigitalOcean app specification found at `bidding-software/lboro-promise-auction.yaml`, which should hopefully rectify any issues.

# How to use the software
- Navigate to the /admin URL (e.g. `http://0.0.0.0:8000/admin` on local) and log in with your superuser account to add items to bid on. You can import `bidding_software/item_import_template.csv` to add some demo data for testing.
- Navigate to the base URL (e.g. `http://0.0.0.0:8000/` on local) to bid on promises.

# Stress-testing the software
- When running on live, it is crucial that you select a powerful enough CPU/database on DigitalOcean.
- Run `python manage.py shell`.
- Paste the contents of `create_stress_test_objects.py` and hit enter.
- Navigate to the website on numerous devices/tabs and check that your CPU/database can handle the resulting large quantity of `update_bids()` AJAX calls from the bidding page.
