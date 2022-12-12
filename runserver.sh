#!/bin/bash

set -ex

path="$(pwd)/djangostock"
cd $path

echo $pwd
source ~/stock_venv/bin/activate

sudo service cron start
python3 manage.py crontab add
python3 manage.py runserver
python3 manage.py crontab remove