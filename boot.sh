#!/bin/bash
python setup.py
exec uvicorn app:connex_app --host 0.0.0.0