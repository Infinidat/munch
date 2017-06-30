default: test

detox-test:
	detox

travis-test: test

test: env
	.env/bin/py.test test_munch.py munch --doctest-modules

coverage-test: env
	.env/bin/coverage run .env/bin/nosetests -w tests

env: .env/.up-to-date

.env/.up-to-date: setup.py Makefile
	virtualenv .env
	.env/bin/pip install -e .
	.env/bin/pip install pytest
	touch .env/.up-to-date

doc: env
	.env/bin/python setup.py build_sphinx

.PHONY: doc
