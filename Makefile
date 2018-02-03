HOST_PYTHON=$(shell which python3.6 || which python 3.5 || false)
VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

PYC=$(shell find . -name '*.pyc')
OK_VENV=.ok_venv
OK_REQ=.ok_req
OK_TESTS=.ok_tests

OK=$(OK_VENV)
OK+=$(OK_REQ)
OK+=$(OK_TESTS)

all: $(OK_TESTS)

clean:
	rm -rf __pycache__
	rm -f $(PYC) $(OK)

envclean:
	rm -rf $(VENV)

run:
	PATH=$(VENV)/bin:$(PATH) FLASK_DEBUG=1 FLASK_APP=main.py flask run --host 0.0.0.0

$(OK_VENV):
	$(HOST_PYTHON) -m venv $(VENV) && touch $@

$(OK_REQ): $(OK_VENV) requirements.txt
	$(PIP) install -r requirements.txt && touch $@

$(OK_TESTS): $(OK_REQ) *.py Makefile
	$(PYTHON) -m unittest discover && touch $@
