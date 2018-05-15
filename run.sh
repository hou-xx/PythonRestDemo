#!/bin/bash
gunicorn exchange:app -p exchange.pid -b 0.0.0.0:8080 -D