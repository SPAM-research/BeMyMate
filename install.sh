#!/bin/sh

# Install python packages
python3 -m venv environment
source bin/activate
pip3 install -r ./base/requirements.txt

# Install ollama
# curl -L https://ollama.ai/download/ollama-linux-amd64 -o ollama
# chmod +x ollama
