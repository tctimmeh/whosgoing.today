PYTHON ?= python3
VENV ?= virtualenv
VENV_DIR ?= venv

VENV_ACTIVATE = . $(VENV_DIR)/bin/activate

setup: venv
	$(VENV_ACTIVATE) && pip install -r pip_requirements.txt
	
venv:
	$(VENV) -p $(PYTHON) $(VENV_DIR)

test:
	whosgoingsite/manage.py test whosgoing
