init:
	pip install -r requirements.txt

test:
	nosetests -v slidown/tests

start:
	python slidown/slidown.py
