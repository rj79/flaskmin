HOST_PYTHON=$(shell which python3.6 || which python 3.5 || false)
VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

SRCS=$(shell find . -name '*.py' | grep -v '\.venv')
PYC=$(shell find . -name '*.pyc')
OK_REQ=.ok_req
OK_TESTS=.ok_tests
OK_VENV=$(VENV)/.ok_venv

OK+=$(OK_REQ)
OK+=$(OK_TESTS)
OK+=$(OK_VENV)

all: $(OK_TESTS)

clean:
	rm -rf __pycache__
	rm -f $(PYC) $(OK)

envclean:
	rm -rf $(VENV)

run: $(OK_TESTS)
	PATH=$(VENV)/bin:$(PATH) FLASK_DEBUG=1 FLASK_APP=main.py flask run --host 0.0.0.0

$(OK_VENV):
	$(HOST_PYTHON) -m venv $(VENV) && touch $(OK_VENV)

$(OK_REQ): $(OK_VENV) requirements.txt
	$(PIP) install -r requirements.txt && touch $@

$(OK_TESTS): $(OK_REQ) $(SRCS) Makefile
	$(PYTHON) -m unittest discover && touch $@
