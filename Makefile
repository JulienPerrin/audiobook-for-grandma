env: 
	virtualenv venv
	source venv/bin/activate

develop:
	python setup.py develop
	pip install -r requirements-dev.txt

pip-local:
	source venv/Scripts/activate
	pip install dist/audiobook-for-grandma-0.1.tar.gz