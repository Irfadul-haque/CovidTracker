@echo off
call .venv\Scripts\activate
pytest tests/test_covid_tracker.py -s
pause
