#!/bin/bash
python setup.py
chmod a+x wof_datasets/wof.db
exec uvicorn app:connex_app --host 0.0.0.0