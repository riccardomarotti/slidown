export PYTHONPATH=$(CURDIR)

tests_command = py.test --cov=slidown --cov-append
init:
	pip3 install -r requirements.txt

git-init:
	git submodule init
	git submodule update

test: clean
	$(tests_command) tests/**

integration: clean
	$(tests_command) integration_tests/**

atest:
	$(tests_command) $(filter-out $@,$(MAKECMDGOALS))

all_tests: test integration

start:
	python3 slidown/main.py

pyinstaller:
	rm -rf build/ dist/
	pyinstaller slidown.spec
	python delete_unused_libraries.py dist/slidown

clean:
	rm -f .coverage
