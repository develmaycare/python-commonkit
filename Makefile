.PHONY: dist docs help tests

# The path to source code to be counted with cloc.
CLOC_PATH := commonkit

# The directory where test coverage is generated.
COVERAGE_PATH := docs/build/html/coverage

# Attempt to load a local makefile which may override any of the values above.
-include local.makefile

#> help - Show help.
help:
	@echo ""
	@echo "Management Commands"
	@echo "------------------------------------------------------------------------------"
	@cat Makefile | grep "^#>" | sed 's/\#\> //g';
	@echo ""

#> dist - Create a distribution of the package.
dist:
	@rm -Rf dist/*;
	python setup.py sdist bdist_wheel;
	twine check dist/*;

#> docs - Generate documentation.
docs: lines
	cd docs && make dirhtml;
	cd docs && make html;
	cd docs && make coverage;
	open docs/build/coverage/python.txt;
	open docs/build/html/index.html;

#> clean - Remove pyc files.
clean:
	find . -name '*.pyc' -delete;
	cd docs && make clean;

# lines - Generate lines of code report.
lines:
	rm -f docs/source/_data/cloc.csv;
	echo "files,language,blank,comment,code" > docs/source/_data/cloc.csv;
	cloc $(CLOC_PATH) --csv --quiet --unix --report-file=tmp.csv 
	tail -n +2 tmp.csv >> docs/source/_data/cloc.csv;
	rm tmp.csv;

#> publish - Publish to PYPI.
publish:
	#twine upload --repository-url https://pypi.org/ dist/*
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

#> secure - Run security checks on the code base.
secure:
	bandit -r $(CLOC_PATH);

#> tests - Run unit tests and generate coverage report.
tests:
	coverage run --source=. -m pytest -s;
	coverage html --directory=$(COVERAGE_PATH);
	open $(COVERAGE_PATH)/index.html;

