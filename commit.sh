#!/bin/bash

find . -name "*.py" -exec sed -i 's/[ \t]*$//' {} +
pylint --rcfile='.pylintrc' 'gramup' 'setup.py' && git commit .
