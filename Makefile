lint:
	flake8 --show-source part_1
	flake8 --show-source part_2
	isort --check-only part_1 --diff
	isort --check-only part_2 --diff
	@echo OK

install:
	pip install -U -r requirements.txt

clean:
	@find . -type f \( -name '*.pyc' -o -name '.DS_Store' \) -delete
	@find . -type d -name '__pycache__' -delete
