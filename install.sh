# install PostgreSQL and PostGIS
sudo apt-get update
sudo apt-get install -y --no-install-recommends postgresql-9.4-postgis-2.1 libpq-dev

# create PostGIS database
sudo sudo -u postgres createuser -s vagrant

sudo sudo -u postgres createdb ognskylines -O vagrant
sudo sudo -u postgres psql -d ognskylines -c 'CREATE EXTENSION postgis;'

# install python3 and pip3
sudo apt-get install -y --no-install-recommends python3 python3-pip

# install python requirements
cd /vagrant
sudo apt-get install -y --no-install-recommends python3-dev libgeos-dev
sudo -H pip3 install -r requirements.txt

# # initialize database
# ./manage.py db.init

# # import registered devices from ddb
# ./manage.py db.import_ddb
