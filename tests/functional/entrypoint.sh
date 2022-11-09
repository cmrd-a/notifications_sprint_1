#!/bin/bash

python redis_waiter.py &&
python es_waiter.py &&
pytest