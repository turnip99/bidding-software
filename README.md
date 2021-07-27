# bidding-software
Django Bidding Software for LSU Christian Union Promise Auction.

# USEFUL COMMANDS

python manage.py runserver
python manage.py runserver 0.0.0.0:8000

sudo systemctl daemon-reload
sudo systemctl restart gunicorn <—— use this one when code changes
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
sudo systemctl status gunicorn

sudo nano /etc/systemd/system/gunicorn.socket
sudo nano /etc/systemd/system/gunicorn.service

Restart nginx: sudo nginx -t && sudo systemctl restart nginx
