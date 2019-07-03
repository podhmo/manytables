test:
	python setup.py test

format:
#	pip install -e .[dev]
	black manytables setup.py

lint:
#	pip install -e .[dev]
	flake8 manytables --ignore W503,E203,E501

build:
#	pip install wheel
	python setup.py bdist_wheel

upload:
#	pip install twine
	twine check dist/manytables-$(shell cat VERSION)*
	twine upload dist/manytables-$(shell cat VERSION)*

.PHONY: test format lint build upload
