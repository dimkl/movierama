MovieRama Project Information


## Requirements
1) python 2.7

2) virtualenv

3) virtualenvwrapper

4) pip > 9


## Local setup project
1) Install virtualenvwrapper: `pip install virtualenvwrapper`

2) Create virtualenv for packages: `mkvirtualenv -a <path_of_extracted_directory> movierama`

3) Enable and go to virtualenv: `workon movierama`

4) Install project requirements: `pip install -r requirements.txt`

5) Run local server: `python manage.py runserver`

6) Browse to localhost:8000


## Testing
1) Execute `python manage.py test`


## Data
1) Admin with username/password: admin/123456qwert
2) load data `python manage.py loaddata _data/users.json _data/movies.json`


## TODO
1) Add email verification on signup
2) Change authentication to JWT for API
