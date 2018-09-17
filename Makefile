.PHONY: help env info clobber test run_test type_check fmt lint

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

env:		## creates a virtual python environment  for this project
	pipenv install --three --dev

info:		## shows current python environment
	pipenv --venv

clobber: clean	## remove virtual python environment
	pipenv --rm

test: fmt run_test

fmt:        ## runs code formatter
	pipenv run yapf --recursive --in-place datadog_deployer


dist: datadog_deployer/*.py README.rst setup.py Pipfile.lock ## create a distribution
	pipenv run python setup.py bdist_wheel

clean:		## remove all intermediate files
	rm -rf datadog_deployer.egg-info
	rm -rf dist build
	find . -name \*.pyc | xargs rm -rf

publish: dist ## publish the package to pypi
	pipenv run twine upload dist/*
