MovieRama Project Information


## Requirements
1) python 2.7

2) virtualenv

3) virtualenvwrapper

4) pip > 9

## Local setup project

1) Create virtualenv for packages: `mkvirtualenv -a <path_of_extracted_directory> movierama`

2) Enable and go to virtualenv: `workon movierama`

3) Install project requirements: `pip install -r requirements.txt`

4) Run local server: `python manage.py runserver`

5) Browse to localhost:8000


## Testing
1) Execute `python manage.py test`


## Data
1) Admin with username/password: admin/123456qwert
2) load data `python manage.py loaddata _data/users.json _data/movies.json`


## Future TODO
1) Add email verification on signup
2) Change authentication to JWT for API
3) Add pagination UI and frontend actions to movies list