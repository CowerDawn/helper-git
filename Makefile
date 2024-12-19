PROGRAM_NAME = helper-git
PYTHON_SCRIPT = main.py
VENV_DIR = .venv

install: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate: requirements.txt
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt
	touch $(VENV_DIR)/bin/activate

run: $(VENV_DIR)/bin/activate
	$(VENV_DIR)/bin/python $(PYTHON_SCRIPT)

clean:
	rm -rf $(VENV_DIR)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: install run clean
