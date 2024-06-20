#!/bin/sh

# Install python packages
python3 -m venv environment
source bin/activate
pip3 install -r ./requirements/base.txt