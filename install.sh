#!/bin/sh

git clone https://gitlab.com/h2282/chatagents
cd chatagents

# Install python packages
python3 -m venv .
source bin/activate
pip3 install -r requirements.txt

# Install ollama
curl -L https://ollama.ai/download/ollama-linux-amd64 -o ollama
chmod +x ollama