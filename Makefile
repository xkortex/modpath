.PHONY: test-all
test-all: mypy xdoctest

.PHONY: fmt
fmt:
	black ./modpath/

.PHONY: mypy
mypy:
	mypy modpath


.PHONY: xdoctest
xdoctest:
	xdoctest modpath
