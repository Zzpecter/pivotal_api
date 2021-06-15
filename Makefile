setup:
	pip install -r requirements.txt

check:
	python -m flake8 main/ --benchmark --statistics
	python -m flake8 tests/ --benchmark --statistics
	python -m pylint main/
	python -m pylint tests/
	python -m pycodestyle main/ --benchmark --statistics
	python -m pycodestyle tests/ --benchmark --statistics

test:
	pytest ./tests -vvv

