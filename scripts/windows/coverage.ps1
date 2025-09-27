python -m pip install coverage
coverage run -m pytest -q
coverage html
coverage report -m

