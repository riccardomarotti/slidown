export PYTHONPATH=./slidown:$PYTHONPATH

tests_command = nosetests -v --with-coverage --cover-package=slidown
init:
	pip3 install -r requirements.txt

git-init:
	git submodule init
	git submodule update

test:
	$(tests_command) tests

integration:
	$(tests_command) **/integration_tests

all_tests: test integration

start:
	python3 slidown/main.py

pyinstaller:
	rm -rf build/ dist/
	pyinstaller slidown.spec
	python delete_unused_libraries.py dist/slidown
