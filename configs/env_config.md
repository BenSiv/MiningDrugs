---
title: Configuration of environment for the data mining project
---

Configuraion of the environment using pip and venv from stand alone installation of python.
Checking the python interpreter.
```bash
python -c 'import sys; print(sys.executable)'
```
```text
/home/bensiv/Python-3.11.0/python
```

Activating current directory as project environment.
```bash
python -m venv .
```

This directory is also a git repository, so I need to add all the non-relevant enviroment directories to gitignore.
```text
.gitignore:
    bin/
    include/
    lib/
    lib64/
    pyvenv.cfg
```
Check that it works.
```bash
git check-ignore *
```
```text
bin
include
lib
pyvenv.cfg
```

Installing packages like: requests
```bash
python -m pip install requests
```

Dump the environment dependencies in to requirements.txt
```bash
python -m pip freeze > requirements.txt
```