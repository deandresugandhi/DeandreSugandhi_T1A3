#!/bin/bash
cd ./src;

if ! [[ -x "$(command -v python3)" ]]
then
  echo 'Error: 
  Python 3 is not installed yet. Please install Python 3 before proceeding.
  You can download and install Python 3 from this link:
  https://www.python.org/downloads/
  Make sure to tick the option to add Python to PATH on installation.' >&2
  exit 1
fi

if ! [[ -x "$(command -v pip)" ]] && ! [[ -x "$(command -v pip3)" ]]; then
  echo 'Error: 
  pip is not installed yet. Please install pip before proceeding.
  You can check how to install pip from this link:
  https://pip.pypa.io/en/stable/installation/' >&2
  exit 1
fi

if [ ! -d "venv" ]
then 
  echo "Creating virtual environment."
  python3 -m venv venv
fi

echo "Activating virtual environment."
source venv/bin/activate
echo "Installing all dependencies before running the application."
pip install -r  ./requirements.txt
echo "Setup completed. Running application."
python3 ./main.py
deactivate
