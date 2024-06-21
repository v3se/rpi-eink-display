#!/bin/bash
set -e 
source venv/bin/activate
python generate-image.py
python image-renderer.py --image sgv_gauge.png
