init:
	pip3 install -r requirements.txt

test:
	nosetests -v **/tests

integration:
	nosetests -v **/integration_tests

start:
	python3 slidown/slidown.py
