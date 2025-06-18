export PYTHONPATH=$(CURDIR)

tests_command = pytest --cov=slidown --cov-append --cov-report=xml

init:
	pip3 install -r requirements.txt

init-dev:
	pip3 install -r requirements-dev.txt

git-init:
	git submodule init
	git submodule update

test: clean
	$(tests_command) tests

integration: clean
	$(tests_command) integration_tests

atest:
	$(tests_command) $(filter-out $@,$(MAKECMDGOALS))

all_tests: test integration

start:
	python3 slidown/main.py

# Install in development mode
install-dev:
	pip install -e .[dev]

# Build Python package
build:
	python -m build

# Build standalone binary with PyInstaller
pyinstaller:
	rm -rf build/ dist/
	pyinstaller slidown.spec
	python delete_unused_libraries.py dist/slidown

# Install from PyPI (when published)
install:
	pip install slidown

clean:
	rm -f .coverage
	rm -rf build/ dist/ *.egg-info/
