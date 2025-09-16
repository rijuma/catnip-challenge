.PHONY: venv install test clean

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Create virtualenv if it doesn't exist and install requirements
venv: requirements.txt
	@test -d $(VENV) || (python3 -m venv $(VENV))
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

# Install dependencies into existing venv
install:
	@$(PIP) install -r requirements.txt

# Run tests inside venv
test:
	@$(PYTHON) -m pytest -v

# Remove venv (for reset)
clean:
	rm -rf $(VENV)
