#!/usr/bin/env bash
if [ "$FLASK_ENV" == "development" ]; then
    echo "installing dev dependencies"
    pipenv lock --requirements --dev > dev-requirements.txt
    pip install --no-cache-dir -r dev-requirements.txt
    rm dev-requirements.txt
fi
exec "$@"