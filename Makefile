init:
	pip install -r requirements.txt

test:
	nosetests -v **/tests

start:
	python slidown/slidown.py
