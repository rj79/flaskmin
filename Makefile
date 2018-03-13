HOST_PYTHON=$(shell which python3.6 || which python 3.5 || false)
VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

SRCS=$(shell find . -name '*.py' | grep -v '\.venv')
PYC=$(shell find . -name '*.pyc')
OK_REQ=.ok_req
OK_TESTS=.ok_tests

OK+=$(OK_REQ)
OK+=$(OK_TESTS)

all: $(OK_TESTS)

clean:
	rm -rf __pycache__
	rm -f $(PYC) $(OK)

envclean:
	rm -rf $(VENV)

run: $(OK_TESTS)
	PATH=$(VENV)/bin:$(PATH) FLASK_DEBUG=1 FLASK_APP=main.py flask run --host 0.0.0.0

$(VENV):
	$(HOST_PYTHON) -m venv $(VENV)

$(OK_REQ): $(VENV) requirements.txt
	$(PIP) install -r requirements.txt && touch $@

$(OK_TESTS): $(OK_REQ) $(SRCS) Makefile
	$(PYTHON) -m unittest discover && touch $@
