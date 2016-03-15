init:
	pip3 install -r requirements.txt
	git submodule init
	git submodule update

test:
	nosetests -v **/tests

integration:
	nosetests -v **/integration_tests

start:
	python3 slidown/slidown.py

pyinstaller:
	rm -rf build/ dist/
	pyinstaller slidown.spec
	python delete_unused_libraries.py dist/slidown
