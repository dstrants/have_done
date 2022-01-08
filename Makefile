cov:
	coverage run -m pytest

report:
	coverage report -m

check-cov: cov report