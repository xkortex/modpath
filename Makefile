.PHONY: test-all
test-all: mypy xdoctest

.PHONY: fmt
fmt:
	black ./modpath/

.PHONY: lint
lint:
	flake8 modpath/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: mypy
mypy:
	mypy modpath


.PHONY: xdoctest
xdoctest:
	xdoctest modpath


.PHONY: test
test:
	pytest


.PHONY: pyinstaller
pyinstaller:
	pyinstaller --onefile modpath/modpath.py
