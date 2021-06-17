setup:
	pip3 install -r requirements.txt

check:
	flake8 main/ --benchmark --statistics
	flake8 tests/ --benchmark --statistics
	pylint main/
	pylint tests/
	pycodestyle main/ --benchmark --statistics
	pycodestyle tests/ --benchmark --statistics

test:
	pytest -vvv --cache-clear --cucumber-json tests/reports/json_test_report.json