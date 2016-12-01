***************************************
# REQUIREMENTS FOR REST API DEVELOPPERS
***************************************
- install Python (download a setup file)
	+ directory named Python à la racine du C:
- installer GIT (download a setup file)

- installer PIP : execute file downloaded at https://bootstrap.pypa.io/get-pip.py (double clic)

- install virtualenv : 
`pip install virtualenvwrapper-win`

- Clone the repository :
`git clone https://github.com/mOscuro/wog_api.git`

- Create a virtual environement folder:
`virtualenv env`

- Activate your virtual environement :
`env\Scripts\activate`

- Install required packages :
`pip install -r requirements.txt`

- Make migrations and fill the database with some data :
```
python manage.py makemigrations
python manage.py migrate
python manage.py create_data
```

- Run the server :
`python manage.py runserver`

Get to work.
