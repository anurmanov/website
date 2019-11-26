# website
The Django project of the website for representing regular company and its goods and services.

The most interesting application of the project is a 'visits' application, because it is intended for tracking visits. The project uses Redis server as cache and storage for statistics of visits. The statistics is divided on different filters (country, city, year, month) via managing redis key names and hash tables.

There is fbb.js module for pop-up sticky feedback JS form in the path ./static/js. All js modules are located in ./static/js path. Most of them use jQuery, but fbb.js (module of the popup sticky feedback form) is implemented according to ES6 standard.

Also the project uses the PostgeSQL database for searchin visister's country and city according to ip-address. This database is based on Geolite2 MaxMind public database. There is a script for moving info from Geolite2 MaxMind public database files to PostgreSQL database.

All potentialy long io-operations (redis, postgres, email interactions) are implemented via Celery tasks. You can observe them in module ./visits/tasks.py
