# wog_api
- installer Python (voir package d'install windows) répertoire Python à la racine du C:
- installer GIT (voir package d'install windows)

- installer PIP : exécuter le fichier téléchargé à l'adresse https://bootstrap.pypa.io/get-pip.py (double clic)

-- installer virtualenv : >> pip install virtualenvwrapper-win
-- installer Django : >> pip install django
-- installer Django Rest Framework : >> pip install djangorestframework
-- installer paquet pour code highlighting : >> pip install pygments

- Instancier le projet :
	>> cd c:\WOG\
	>> django-admin.py startproject wogether
	>> cd wogether

********************************
	REQUIREMENTS FOR REACTJS	
********************************

* Node.js & npm >> https://nodejs.org/en/

* Babel
	>> npm install -g babel
	>> npm install -g babel-cli

* Create Root Folder
	>> mkdir reactApp
	>> npm init

* Webpack
	>> npm install webpack --save
	>> npm install webpack-dev-server --save

* React
	>> npm install react --save
	>> npm install react-dom --save

* Babel plugin
	>> npm install babel-core
	>> npm install babel-loader
	>> npm install babel-preset-react
	>> npm install babel-preset-es2015

****************************
	SUBLIME TEXT SETUPS
****************************
- Emmet : (https://github.com/sergeche/emmet-sublime)
	+ Plugin installation dans Sumblime Text : "Emmet"
	
- Linter : (https://github.com/SublimeLinter/SublimeLinter-jshint)
	>> npm install -g jshint
	+ Plugin installation dans Sumblime Text : "SublimeLinter-jshint"
	+ Settings for EsLint : https://codepen.io/mi-lee/post/sublime-text-setup-for-react-js-development
	
- JsFormat : (https://github.com/jdc0589/JsFormat)
	+ Plugin installation dans Sumblime Text : "JsFormat"
