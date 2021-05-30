.PHONY: dist docs help tests

# The path to source code to be counted with cloc.
PACKAGE_NAME := commonkit

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
	cp DESCRIPTION.txt $(PACKAGE_NAME)/;
	cp LICENSE.txt $(PACKAGE_NAME)/;
	cp VERSION.txt $(PACKAGE_NAME)/;
	@rm -Rf build/*;
	@rm -Rf dist/*;
	@rm -Rf *.egg-info;
	python setup.py sdist bdist_wheel;
	twine check dist/*;
	rm $(PACKAGE_NAME)/*.txt;

#> docs - Generate documentation.
docs: lines
	cd docs && make dirhtml;
	cd docs && make html;
	cd docs && make json;
	cd docs && make coverage;
	mkdir docs/build/json/coverage;
	cp docs/build/html/coverage/index.html docs/build/json/coverage/;
	open docs/build/coverage/python.txt;
	open docs/build/html/index.html;

#> clean - Remove pyc files and documentation builds.
clean:
	find . -name '*.pyc' -delete;
	cd docs && make clean;

# lines - Generate lines of code report.
lines:
	rm -f docs/source/_data/cloc.csv;
	echo "files,language,blank,comment,code" > docs/source/_data/cloc.csv;
	cloc $(PACKAGE_NAME) --csv --quiet --unix --report-file=tmp.csv 
	tail -n +2 tmp.csv >> docs/source/_data/cloc.csv;
	rm tmp.csv;

#> publish - Publish to PYPI.
publish:
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*;
	#twine upload --repository-url https://test.pypi.org/legacy/ dist/*


#> secure - Run security checks on the code base.
secure:
	bandit -r $(PACKAGE_NAME);

#> tests - Run unit tests and generate coverage report.
tests:
	cd tests/watched && ln -s nonexistent.md
	cd tests/watched && ln -s nonexistent.txt
	coverage run --source=. -m pytest -s;
	coverage html --directory=$(COVERAGE_PATH);
	open $(COVERAGE_PATH)/index.html;
	rm tests/watched/nonexistent.md;
	rm tests/watched/nonexistent.txt;

