@echo off
py -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo Virtual environment is ready.
echo Run: .venv\Scripts\activate && python main.py

