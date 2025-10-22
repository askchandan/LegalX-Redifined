#!/bin/bash
# Install setuptools first to avoid build_meta import errors
pip install setuptools>=65.0.0 wheel
# Then install the rest of the requirements
pip install -r requirements.txt